""" Представления для курсов, уроков и подписок"""
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Course, Lesson, Subscription
from .pagination import CoursePagination, LessonPagination, SubscriptionPagination
from .permissions import IsCourseOwner, IsModerator, IsLessonOwner, IsSubscriptionOwner
from .serializers import CourseSerializer, LessonSerializer, CourseListSerializer, \
    CourseDetailSerializer, SubscriptionSerializer, LessonListSerializer
from rest_framework import generics
from training_courses.tasks import send_lesson_update_emails, send_course_update_emails


class CourseViewSet(viewsets.ModelViewSet):
    """ ViewSet для курсов """
    queryset = Course.objects.all().order_by('pk')
    default_serializer = CourseSerializer
    pagination_class = CoursePagination
    list_serializers = {
        "list": CourseListSerializer,
        "retrieve": CourseDetailSerializer,
        "create": CourseSerializer,
        "update": CourseSerializer,
        "destroy": CourseSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        course_id = self.get_object().id
        send_course_update_emails.delay(course_id)

    def get_serializer_class(self):
        return self.list_serializers.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.annotate(lessons_count=Count("lesson"))
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsAuthenticated, IsCourseOwner | IsModerator]
        if self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsCourseOwner | IsModerator]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'update':
            self.permission_classes = [IsAuthenticated, IsCourseOwner]
        else:
            self.permission_classes = [IsAuthenticated, IsCourseOwner | IsAdminUser]

        return super().get_permissions()


class SubscriptionViewSet(viewsets.ModelViewSet):
    """ ViewSet для подписок """
    queryset = Subscription.objects.all().order_by('pk')
    serializer_class = SubscriptionSerializer
    pagination_class = SubscriptionPagination
    permission_classes = [IsAuthenticated, IsSubscriptionOwner | IsModerator]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """ Список уроков """
    serializer_class = LessonListSerializer
    queryset = Lesson.objects.all().order_by('pk')
    permission_classes = [IsAuthenticated, IsLessonOwner | IsModerator]
    pagination_class = LessonPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """ Подробная информация об уроке """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all().order_by('pk')
    permission_classes = [IsAuthenticated, IsLessonOwner | IsModerator]


class LessonCreateAPIView(generics.CreateAPIView):
    """ Создание урока """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)
        course_id = lesson.course.id if lesson.course else None
        if course_id:
            send_course_update_emails.delay(course_id)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """ Обновление урока """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all().order_by('pk')
    permission_classes = [IsAuthenticated, IsLessonOwner]

    def perform_update(self, serializer):
        lesson_id = self.get_object().id
        course_id = self.get_object().course.id if self.get_object().course else None
        send_lesson_update_emails.delay(lesson_id)
        if course_id:
            send_course_update_emails.delay(course_id)
        return super().perform_update(serializer)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """ Удаление урока """
    queryset = Lesson.objects.all().order_by('pk')
    permission_classes = [IsAuthenticated, IsLessonOwner | IsAdminUser]
