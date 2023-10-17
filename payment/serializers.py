""" Сериалайзеры для payment """
from rest_framework import serializers
from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """ Сериалайзер оплаты """
    class Meta:
        """ Мета-данные """
        model = Payment
        fields = '__all__'
