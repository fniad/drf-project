""" Права доступа в приложении training_courses """
from rest_framework.permissions import BasePermission

import users.models


class IsLessonOwner(BasePermission):
    """ Только для владельцев урока """
    message = 'Вы не владелец урока'
    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False


class IsCourseOwner(BasePermission):
    """ Только для владельцев курса"""
    message = 'Вы не владелец курса'
    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False


class IsSubscriptionOwner(BasePermission):
    """ Только для владельцев подписки """
    message = 'Вы не владелец подписки'
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        return False


class IsModerator(BasePermission):
    """ Только для модератора """
    message = 'Только модератор'

    def has_permission(self, request, view):
        if request.user.role == users.models.UserRoles.MODERATOR:
            return True
        return False
