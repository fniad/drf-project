from rest_framework import serializers
from rest_framework.fields import IntegerField

from training_courses.models import Course, Lesson
from training_courses.validators import LinkValidator


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        validators = {
             LinkValidator(field='description_course')
        }


class CourseListSerializer(serializers.ModelSerializer):
    lessons_count = IntegerField()

    class Meta:
        model = Course
        fields = ('name_course', 'lessons_count',)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = {
            LinkValidator(field='video_url_lesson'),
            LinkValidator(field='description_lesson')
        }


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('name_lesson',)


class CourseDetailSerializer(serializers.ModelSerializer):
    lesson_in_this_course = LessonSerializer(source="lesson_set", many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
