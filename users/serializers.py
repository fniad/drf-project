from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from payment.models import Payment
from payment.serializers import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payments_this_user = SerializerMethodField()

    def get_payments_this_user(self, user):
        return PaymentSerializer(Payment.objects.filter(user=user), many=True).data

    class Meta:
        model = User
        fields = '__all__'
