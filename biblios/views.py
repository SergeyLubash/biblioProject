from rest_framework.viewsets import ModelViewSet

from biblios.models import Author, Books, Readers
from biblios.permissions import PermissionPolicyMixin, IsOwner
from biblios.serializers import AuthorSerializer, BooksSerializer, ReadersSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser


class AuthorViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes_per_method = {
        'list': [AllowAny],
        'create': [IsAdminUser],
        'update': [IsAdminUser],
        'destroy': [IsAdminUser],
    }
# 1. **CREATE**: создавать объекты может только администратор
# 2. **READ**: получать данные об объекте могут все
# 3. **UPDATE**: обновлять объекты может только администратор
# 4. **DELETE**: удалять объекты может только администратор


class BooksViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes_per_method = {
        'list': [AllowAny],
        'create': [IsAdminUser],
        'update': [IsAdminUser],
        'destroy': [IsAdminUser],
    }

# 1. **CREATE**: создавать объекты может только администратор
# 2. **READ**: получать данные об объекте могут все
# 3. **UPDATE**: обновлять объекты может только администратор
# 4. **DELETE**: удалять объекты может только администратор


class ReadersViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = Readers.objects.all()
    serializer_class = ReadersSerializer
    permission_classes_per_method = {
        'list': [IsAdminUser, IsOwner],
        'create': [AllowAny],
        'update': [IsAdminUser, IsOwner],
        'destroy': [IsAdminUser, IsOwner],
    }

# 1. **CREATE**: создавать объекты могут все пользователи без авторизации
# 2. **READ**: получать данные об объекте может администратор и пользователь, который запрашивает свои данные
# 3. **UPDATE**: обновлять объекты может администратор и пользователь, который изменяет свои данные
# 4. **DELETE**: удалять объекты может администратор и пользователь, который удаляет свои данные
