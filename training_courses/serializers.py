""" Сериалайзеры приложения training_courses """
from rest_framework import serializers
from rest_framework.fields import IntegerField

from training_courses.models import Course, Lesson, Subscription
from training_courses.validators import LinkValidator


class CourseSerializer(serializers.ModelSerializer):
    """ Сериалайзер курса """
    class Meta:
        """ Мета-данные """
        model = Course
        fields = '__all__'
        extra_kwargs = {
            'owner': {'required': False}
        }
        validators = {
             LinkValidator(field='description_course')
        }


class CourseListSerializer(serializers.ModelSerializer):
    """ Сериалайзер для вывода списка курсов"""
    lessons_count = IntegerField()
    subscription = serializers.SerializerMethodField(read_only=True)

    def get_subscription(self, obj):
        """ Получение подписки на курс """
        user = self.context['request'].user
        if Subscription.objects.filter(user=user, course=obj).exists():
            return 'подписан'
        return 'не подписан'

    class Meta:
        """ Мета-данные """
        model = Course
        fields = ('name_course', 'lessons_count', 'subscription')


class LessonSerializer(serializers.ModelSerializer):
    """ Сериалайзер урока """
    class Meta:
        """ Мета-данные """
        model = Lesson
        fields = '__all__'
        extra_kwargs = {
            'owner': {'required': False}
        }
        validators = {
            LinkValidator(field='video_url_lesson'),
            LinkValidator(field='description_lesson')
        }


class LessonListSerializer(serializers.ModelSerializer):
    """ Сериалайзер для списка уроков """
    subscription = serializers.SerializerMethodField(read_only=True)

    def get_subscription(self, obj):
        """ Получение подписки на урок """
        user = self.context['request'].user
        if Subscription.objects.filter(user=user, lesson=obj).exists():
            return 'подписан'
        return 'не подписан'

    class Meta:
        """ Мета-данные """
        model = Lesson
        fields = ('name_lesson', 'subscription')


class CourseDetailSerializer(serializers.ModelSerializer):
    """ Серилайзер для страницы курса """
    lesson_in_this_course = LessonSerializer(source="lesson_set", many=True, read_only=True)

    class Meta:
        """ Мета-данные """
        model = Course
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    """ Сериалайзер для подписок """
    class Meta:
        """ Мета-данные """
        model = Subscription
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False}
        }
