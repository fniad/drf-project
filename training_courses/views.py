from django.db.models import Count
from rest_framework import viewsets, generics
from training_courses.models import Course, Lesson
from training_courses.serializers import CourseSerializer, LessonSerializer, CourseListSerializer, \
    CourseDetailSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    default_serializer = CourseSerializer
    list_serializers = {
        "list": CourseListSerializer,
        "retrieve": CourseDetailSerializer,
    }

    def get_serializer_class(self):
        return self.list_serializers.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.annotate(lessons_count=Count("lesson"))
        return super().list(request, *args, **kwargs)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
