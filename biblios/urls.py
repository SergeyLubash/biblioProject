from rest_framework import routers

from .views import AuthorViewSet, BooksViewSet, ReadersViewSet

router = routers.DefaultRouter()
router.register(r'author', AuthorViewSet)
router.register(r'books', BooksViewSet)
router.register(r'readers', ReadersViewSet)
