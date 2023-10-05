from rest_framework import serializers
from rest_framework.fields import IntegerField, SerializerMethodField

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'
