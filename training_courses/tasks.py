""" Задачи celery """
from celery import shared_task
from training_courses.models import Subscription, Course, Lesson
from training_courses.services import send_subscription_email
from django.utils import timezone
from users.models import User
from datetime import datetime, timedelta


@shared_task
def send_course_update_emails(course_id):
    """ Отправка уведомления об изменении курса """
    course = Course.objects.get(id=course_id)
    last_update_time = course.last_update
    if last_update_time < timezone.now() - timedelta(hours=4):
        subscriptions = Subscription.objects.filter(course=course, is_active=True)
        for subscription in subscriptions:
            user = subscription.user
            subject = 'Обновление курса, на который вы подписаны'
            message = f'Здравствуйте, {user.username}, курс {course.name_course} был обновлён!'
            send_subscription_email(user, subject, message)


@shared_task
def send_lesson_update_emails(lesson_id):
    """ Отправка уведомления об изменении урока """
    lesson = Lesson.objects.get(id=lesson_id)
    if not lesson.course:  # Проверяем, что урок не включен в курс
        last_update_time = lesson.last_update
        if last_update_time < timezone.now() - timedelta(hours=4):
            subscriptions = Subscription.objects.filter(lesson=lesson, is_active=True)
            for subscription in subscriptions:
                user = subscription.user
                subject = 'Обновление урока, на который вы подписаны'
                message = f'Здравствуйте, {user.username}, урок {lesson.name_lesson} был обновлён!'
                send_subscription_email(user, subject, message)


@shared_task
def check_inactive_users():
    """ Проверка активности пользователей """
    inactive_users = User.objects.filter(last_login__lt=datetime.now() - timedelta(days=30), is_active=True)
    for user in inactive_users:
        user.is_active = False
        user.save()
