from django.urls import path

from payment.apps import PaymentConfig
from payment.views import *

app_name = PaymentConfig.name

urlpatterns = [
    path('payments/', PaymentListAPIView.as_view(), name='list-payment'),
    path('payments/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='view-payment'),
    path('payments/create/', PaymentCreateAPIView.as_view(), name='create-payment'),
    path('payments/update/<int:pk>/', PaymentUpdateAPIView.as_view(), name='update-payment'),
    path('payments/delete/<int:pk>/', PaymentDestroyAPIView.as_view(), name='delete-payment'),
]
