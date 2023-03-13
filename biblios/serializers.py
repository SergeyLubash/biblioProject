from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from biblios.models import Author, Books, Readers


class Phonevalidator:

    def __call__(self, value):
        phone_number = str(value)
        if not phone_number.startswith("7"):
            raise serializers.ValidationError("Номер телефона должен начинаться с 7")
        if len(phone_number) != 11:
            raise serializers.ValidationError("Номер телефона должен содержать 11 цифр")
        if not phone_number.isdigit():
            raise serializers.ValidationError("Номер телефона должен содержать только цифры")
        return value


class Numberpagesvalidator:

    def __call__(self, value):
        if value < 0:
            raise serializers.ValidationError("Количество страниц не может быть отрицательным числом")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'first_name', 'last_name', 'photo', 'created_at', 'updated_at')


class BooksSerializer(serializers.ModelSerializer):
    number_pages = serializers.IntegerField(validators=[Numberpagesvalidator()])
    author = serializers.SlugRelatedField(
        queryset=Author.objects.all(),
        slug_field='last_name'
    )

    class Meta:
        model = Books
        fields = ('id', 'title', 'description', 'number_pages', 'author', 'quantity', 'created_at', 'updated_at')
        read_only_fields = ['author']


class ReadersSerializer(serializers.ModelSerializer):
    phone = serializers.IntegerField(validators=[Phonevalidator()])
    activ_books = serializers.SlugRelatedField(
        queryset=Books.objects.all(),
        slug_field='title',
        many=True,
        validators=['booklimit', 'update']
    )

    def booklimit(self, attrs):
        if len(attrs['activ_books']) > 3:
            raise serializers.ValidationError('В одни руки не более 3 книг')
        return attrs

    def create(self, validated_data):
        readers = super().create(validated_data)
        readers.set_password(readers.password)
        readers.save()

        if validated_data['activ_books']:
            for book in validated_data['activ_books']:
                if book.quantity == 0:
                    raise serializers.ValidationError(f'Книги {book} нет в наличии')

        books_data = validated_data.pop('activ_books')
        reader = Readers.objects.create(**validated_data)
        for book_data in books_data:
            book = Books.objects.get(pk=book_data.id)
            if book.quantity > 0:
                book.quantity -= 1
                book.save()
                reader.activ_books.add(book)
            else:
                raise serializers.ValidationError(f'Книга {book.title} отсутствует')
        return reader

    def update(self, instance, validated_data):
        if validated_data['activ_books']:
            for book in validated_data['activ_books']:
                if book not in instance.activ_books.all():
                    if book.quantity > 0:
                        book.quantity -= 1
                        book.save()
                    else:
                        raise serializers.ValidationError(f'Книга {book.title} отсутствует')
            for book in instance.activ_books.all():
                if book not in validated_data['activ_books']:
                    book.quantity += 1
                    book.save()
        return super().update(instance, validated_data)

    class Meta:
        model = Readers
        fields = '__all__'
