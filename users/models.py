from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')


class User(AbstractUser):
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} - {self.role}"

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
