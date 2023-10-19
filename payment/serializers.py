""" Сериалайзеры для payment """
import stripe
from django.conf import settings
from rest_framework import serializers
from payment.models import Payment, StripeCheckoutSession
from training_courses.serializers import CourseSerializer, LessonSerializer


stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentSerializer(serializers.ModelSerializer):
    """ Информация об оплате """
    content_type = serializers.CharField(write_only=True)
    object_id = serializers.IntegerField(write_only=True)
    course = serializers.SerializerMethodField(read_only=True)
    lesson = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_course(obj):
        """ Подробная информация курса """
        if obj.content_type.model == 'course':
            course = obj.content_object
            return CourseSerializer(course).data
        return None

    @staticmethod
    def get_lesson(obj):
        """ Подробная информация урока """
        if obj.content_type.model == 'lesson':
            lesson = obj.content_object
            return LessonSerializer(lesson).data
        return None

    class Meta:
        """ Мета-данные """
        model = Payment
        fields = ['user', 'date_pay', 'payment_amount', 'payment_method', 'content_type', 'object_id', 'course',
                  'lesson']


class PaymentRetrieveSerializer(serializers.ModelSerializer):
    """ Подробная информация оплаты """
    content_type = serializers.CharField(write_only=True)
    object_id = serializers.IntegerField(write_only=True)
    course = serializers.SerializerMethodField(read_only=True)
    lesson = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_course(obj):
        """ Подробная информация курса """
        if obj.content_type.model == 'course':
            course = obj.content_object
            return CourseSerializer(course).data
        return None

    @staticmethod
    def get_lesson(obj):
        """ Подробная информация урока """
        if obj.content_type.model == 'lesson':
            lesson = obj.content_object
            return LessonSerializer(lesson).data
        return None

    class Meta:
        """ Мета-данные """
        model = Payment
        fields = ['user', 'date_pay', 'payment_amount', 'payment_method', 'content_type', 'object_id', 'course',
                  'lesson']


class StripeCheckoutSessionSerializer(serializers.ModelSerializer):
    """ Проверка сессии платежа """
    product = serializers.StringRelatedField()

    class Meta:
        """ Мета-данные """
        model = StripeCheckoutSession
        fields = ('uid', 'product', 'status', 'stripe_id', 'payment')


class SuccessPaymentSerializer(serializers.ModelSerializer):
    """ Подробная информация оплаты """
    class Meta:
        """ Мета-данные """
        model = Payment
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False}
        }
