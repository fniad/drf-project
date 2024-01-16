""" URLS для приложения users """
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView

app_name = UsersConfig.name


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/create/', UserCreateAPIView.as_view(), name='create'),
    path('user/<int:pk>/', UserRetrieveAPIView.as_view(), name='view'),
    path('user/update/<int:pk>/', UserUpdateAPIView.as_view(), name='update'),
    path('user/delete/<int:pk>/', UserDestroyAPIView.as_view(), name='delete'),
    path('user/', UserListAPIView.as_view(), name='list'),
]
