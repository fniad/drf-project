from rest_framework import serializers
from rest_framework.fields import IntegerField, SerializerMethodField

from training_courses.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class CourseListSerializer(serializers.ModelSerializer):
    lessons_count = IntegerField()

    class Meta:
        model = Course
        fields = ('name_course', 'lessons_count', )


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ('name_lesson', )


class CourseDetailSerializer(serializers.ModelSerializer):
    lesson_in_this_course = LessonSerializer(source="lesson_set", many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
