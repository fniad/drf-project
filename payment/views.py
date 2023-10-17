""" Представления для payments """
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from payment.models import Payment
from payment.serializers import PaymentSerializer


class PaymentListAPIView(generics.ListAPIView):
    """ Список оплат отсортированный по датам, с фильтрами по курсам, урокам и методу оплаты"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all().order_by('date_pay')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method', )
    ordering_fields = ('date_pay', )
    permission_classes = [IsAuthenticated]


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """ Подробная информация оплаты """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all().order_by('date_pay')
    permission_classes = [IsAuthenticated]


class PaymentCreateAPIView(generics.CreateAPIView):
    """ Создание оплаты """
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class PaymentUpdateAPIView(generics.UpdateAPIView):
    """ Изменение оплаты """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all().order_by('date_pay')
    permission_classes = [IsAuthenticated]


class PaymentDestroyAPIView(generics.DestroyAPIView):
    """ Удаление оплаты """
    queryset = Payment.objects.all().order_by('date_pay')
    permission_classes = [IsAuthenticated]
