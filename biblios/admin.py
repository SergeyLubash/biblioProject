from django.contrib import admin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.html import format_html

from biblios.models import Author, Readers, Books


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'photo')
    list_display_links = ('first_name', 'last_name')
    search_fields = ('last_name',)


class BooksAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'number_pages', 'author_link', 'quantity')
    search_fields = ('title',)
    actions = ['quantity_none']

    @admin.action(description='Изменения наличия книг')
    def quantity_none(self, request, queryset: QuerySet):
        queryset.update(quantity=0)

    def author_link(self, obj):
        author = obj.author
        url = reverse("admin:bibliotek_author_changelist") + str(author.pk)
        return format_html(f'<a href="{url}">{author}</a>')

    author_link.short_description = 'Авторы'


class ReadersAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'display_activ_books')
    # list_filter = ('status',)
    list_display_links = ('last_name',)
    actions = ['activ_books_clear']

    # @admin.action(description='Статус активности читателя')
    # def status(self, request, queryset: QuerySet):
    #     queryset.update(status=False)

    @admin.action(description='Удаления всех книг у пользователя')
    def activ_books_clear(self, request, queryset):
        for clearing in queryset:
            clearing.activ_books.clear()


admin.site.register(Readers, ReadersAdmin)
admin.site.register(Books, BooksAdmin)
admin.site.register(Author, AuthorAdmin)
