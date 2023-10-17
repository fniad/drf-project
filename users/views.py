""" Представления для users """
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from users.models import User
from users.pagination import UserPagination
from users.permissions import IsOwnerOrReadOnly
from users.serializers import UserSerializer, UserPublicProfileSerializer, UserCreateSerializer, UserProfileSerializer


class UserListAPIView(generics.ListAPIView):
    """ Список уроков """
    serializer_class = UserPublicProfileSerializer
    queryset = User.objects.all().order_by('pk')
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = UserPagination


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """ Подробная информация об уроке """
    queryset = User.objects.all().order_by('pk')
    pagination_class = UserPagination
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly | IsAdminUser]

    def get_serializer_class(self):
        """ Получение сериализаторов """
        if self.request.user.is_authenticated:
            if self.request.user.is_staff or self.get_object().id == self.request.user.id:
                return UserProfileSerializer
        return UserPublicProfileSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """ Создание урока """
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class UserUpdateAPIView(generics.UpdateAPIView):
    """ Обновление урока """
    queryset = User.objects.all().order_by('pk')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly | IsAdminUser]


class UserDestroyAPIView(generics.DestroyAPIView):
    """ Удаление урока """
    queryset = User.objects.all().order_by('pk')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly | IsAdminUser]
