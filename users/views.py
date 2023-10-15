from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.permissions import IsOwnerOrReadOnly
from users.serializers import UserSerializer, UserPublicProfileSerializer, UserCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        else:
            return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return UserPublicProfileSerializer
        elif (self.action in ['retrieve', 'update', 'partial_update', 'destroy'] and
              self.request.user == self.get_object() or self.request.user.is_superuser):
            return UserSerializer
        elif self.action == 'retrieve' and self.request.user != self.get_object():
            return UserPublicProfileSerializer
        elif self.action == 'create':
            return UserCreateSerializer
