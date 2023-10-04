from django.urls import path
from rest_framework.routers import DefaultRouter

from training_courses.apps import TrainingCoursesConfig
from training_courses.views import *

app_name = TrainingCoursesConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
                  path('lessons/', LessonListAPIView.as_view(), name='list-lessons'),
                  path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='view-lesson'),
                  path('lessons/create/', LessonCreateAPIView.as_view(), name='create-lessons'),
                  path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='update-lessons'),
                  path('lessons/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='delete-lessons'),

              ] + router.urls
