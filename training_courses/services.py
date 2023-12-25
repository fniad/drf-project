""" Сервисные функции """
from django.conf import settings
from django.core.mail import send_mail


def send_subscription_email(user, subject, message):
    """ Отправка письма по подписке """
    from_email = settings.EMAIL_HOST_USER
    to_email = user.email
    send_mail(
        f"{subject}",
        f"{message}",
        f"{from_email}",
        [f"{to_email}"],
        fail_silently=False,
    )
