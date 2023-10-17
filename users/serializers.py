""" Сериалайзеры для users """
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from payment.models import Payment
from payment.serializers import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Сериалайзер пользователя """
    payments_this_user = SerializerMethodField()

    def get_payments_this_user(self, user):
        """ Получение оплат пользователя """
        return PaymentSerializer(Payment.objects.filter(user=user), many=True).data

    class Meta:
        """ Мета-данные """
        model = User
        fields = '__all__'


class UserPublicProfileSerializer(serializers.ModelSerializer):
    """ Сериалайзер публичной информации о пользователе """
    class Meta:
        """ Мета-данные """
        model = User
        fields = ('username', 'first_name')


class UserProfileSerializer(serializers.ModelSerializer):
    """ Сериалайзер личной информации о пользователе """
    class Meta:
        """ Мета-данные """
        model = User
        fields = ('__all__')



class UserCreateSerializer(serializers.ModelSerializer):
    """ Сериалайзер создания пользователя """
    class Meta:
        """ Мета-данные """
        model = User
        fields = ('email', 'username', 'password')
