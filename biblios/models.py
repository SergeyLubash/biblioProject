from django.db import models
from django.contrib.auth.models import AbstractUser


class Author(models.Model):
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    photo = models.ImageField(upload_to='photos/', blank=True, verbose_name='Фото')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Books(models.Model):
    title = models.CharField(max_length=20, verbose_name='Название')
    description = models.TextField(max_length=300, verbose_name='Описание')
    number_pages = models.IntegerField(verbose_name='Кол-во станиц')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, help_text='Выберите автора книги', verbose_name='Автор')
    quantity = models.IntegerField(blank=True, verbose_name='Кол-во книг в библиотеке')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['title']

    def __str__(self):
        return f'{self.title}'


class Readers(AbstractUser):
    # first_name = models.CharField(max_length=20, verbose_name='Имя')
    # last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    phone = models.BigIntegerField(verbose_name='Номер телефона')
    # status = models.BooleanField(default=True, verbose_name='Статус читателя')
    activ_books = models.ManyToManyField(Books, blank=True, verbose_name='Активные книги')
    # created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')

    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'
        ordering = ['username']

    def __str__(self):
        return self.username

    def display_activ_books(self):
        return ', '.join([activ_book.title for activ_book in self.activ_books.all()])

    display_activ_books.short_description = 'Активные книги'
