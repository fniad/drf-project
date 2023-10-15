from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsOwnerOrReadOnly(permissions.BasePermission):
    """ Права доступа для владельцев или для чтения"""

    message = "У Вас не достаточно прав для доступа!"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user == view.get_object():
            return True
        return False
