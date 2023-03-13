from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = 'No access'

    def has_permission(self, request, view):
        if request.user.id == int(view.kwargs['pk']):
            return True
        return False

    
class PermissionPolicyMixin:
    def check_permissions(self, request):
        try:
            handler = getattr(self, request.method.lower())
        except AttributeError:
            handler = None

        if handler and self.permission_classes_per_method and self.permission_classes_per_method.get(handler.__name__):
            self.permission_classes = self.permission_classes_per_method.get(handler.__name__)

        super().check_permissions(request)
