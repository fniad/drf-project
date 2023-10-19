import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from users.models import NULLABLE, User


def get_default_content_type():
    """ Получение ID контент-типа по умолчанию """
    course_content_type = ContentType.objects.get(app_label='training_courses', model='course')
    return course_content_type.id


class Payment(models.Model):
    """ Модель оплаты """
    PAY_CARD = 'card'
    PAY_CASH = 'cash'

    PAYMENT_TYPES = (
        (PAY_CARD, 'картой'),
        (PAY_CASH, 'наличными')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    date_pay = models.DateField(auto_now_add=True, verbose_name='дата оплаты')
    payment_amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    payment_method = models.CharField(choices=PAYMENT_TYPES, default=PAY_CASH,
                                      max_length=100, verbose_name='способ оплаты')
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        default=get_default_content_type,
        limit_choices_to=models.Q(app_label='training_courses', model='course') | models.Q(app_label='training_courses',
                                                                                           model='lesson'),
    )
    object_id = models.PositiveIntegerField(verbose_name='ID объекта', **NULLABLE)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.user} - {self.date_pay}'

    class Meta:
        """ Мета-данные """
        verbose_name = 'оплата'
        verbose_name_plural = 'оплаты'


class StripeCheckoutSession(models.Model):
    """ Модель сессии оплаты Stripe """
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stripe_id = models.CharField(max_length=255, unique=True, editable=False)
    status = models.CharField(max_length=10)
    customer_email = models.EmailField(null=True, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, verbose_name='платеж')
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        default=get_default_content_type,
        limit_choices_to=models.Q(app_label='training_courses', model='course') | models.Q(app_label='training_courses',
                                                                                           model='lesson'),
    )

    def __str__(self):
        return f'{self.payment} - {self.stripe_id}'

    class Meta:
        """ Мета-данные """
        verbose_name = 'сессия оплаты Stripe'
        verbose_name_plural = 'сессии оплаты Stripe'
