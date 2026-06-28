from rest_framework.permissions import BasePermission
from .models import User

class Isadmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role=="admin"
        )
class Iscustomer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role=="customer"
        )
class Isprovider(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role=="provider"
        )