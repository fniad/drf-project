from django.db.models import Count
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from training_courses.models import Course, Lesson
from training_courses.serializers import CourseSerializer, LessonSerializer, CourseListSerializer, \
    CourseDetailSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('name_course')
    default_serializer = CourseSerializer
    list_serializers = {
        "list": CourseListSerializer,
        "retrieve": CourseDetailSerializer,
    }
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return self.list_serializers.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.annotate(lessons_count=Count("lesson"))
        return super().list(request, *args, **kwargs)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
