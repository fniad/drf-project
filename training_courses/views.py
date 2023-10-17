""" Представления для курсов, уроков и подписок"""
from django.db.models import Count
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Course, Lesson, Subscription
from .pagination import CoursePagination, LessonPagination, SubscriptionPagination
from .permissions import IsCourseOwner, IsModerator, IsLessonOwner, IsSubscriptionOwner
from .serializers import CourseSerializer, LessonSerializer, CourseListSerializer, \
    CourseDetailSerializer, SubscriptionSerializer, LessonListSerializer


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
        serializer.save(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """ Обновление урока """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all().order_by('pk')
    permission_classes = [IsAuthenticated, IsLessonOwner | ~IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """ Удаление урока """
    queryset = Lesson.objects.all().order_by('pk')
    permission_classes = [IsAuthenticated, IsLessonOwner | IsAdminUser]
