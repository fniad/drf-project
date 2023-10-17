""" URLS для приложения payment """
from django.urls import path

from payment.apps import PaymentConfig
from payment.views import *

app_name = PaymentConfig.name

urlpatterns = [
    path('', PaymentListAPIView.as_view(), name='list-payment'),
    path('<int:pk>/', PaymentRetrieveAPIView.as_view(), name='view-payment'),
    path('create/', PaymentCreateAPIView.as_view(), name='create-payment'),
    path('update/<int:pk>/', PaymentUpdateAPIView.as_view(), name='update-payment'),
    path('delete/<int:pk>/', PaymentDestroyAPIView.as_view(), name='delete-payment'),
]
