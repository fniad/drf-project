""" URLs training_courses """
from django.urls import path
from rest_framework.routers import DefaultRouter

from training_courses.apps import TrainingCoursesConfig
from training_courses.views import *

app_name = TrainingCoursesConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'subscription', SubscriptionViewSet, basename='subscription')

urlpatterns = [
                  path('lesson/', LessonListAPIView.as_view(), name='list-lessons'),
                  path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='view-lesson'),
                  path('lesson/create/', LessonCreateAPIView.as_view(), name='create-lessons'),
                  path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='update-lessons'),
                  path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='delete-lessons'),

              ] + router.urls
