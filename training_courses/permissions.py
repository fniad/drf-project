from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsLessonOwner(BasePermission):
    message = 'Вы не владелец урока'
    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False


class IsCourseOwner(BasePermission):
    message = 'Вы не владелец курса'
    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False


class IsSubscriptionOwner(BasePermission):
    message = 'Вы не владелец подписки'
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        return False


class IsModerator(BasePermission):
    message = 'Только модератор'

    def has_permission(self, request, view):
        if request.user.role == UserRoles.MODERATOR:
            return True
        return False


