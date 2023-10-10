from django.db import models

from training_courses.models import Course, Lesson
from users.models import NULLABLE, User


class Payment(models.Model):
    PAY_CARD = 'card'
    PAY_CASH = 'cash'

    PAYMENT_TYPES = (
        (PAY_CARD, 'картой'),
        (PAY_CASH, 'наличными')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, related_name='payment')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE, related_name='payment')
    date_pay = models.DateField(auto_now_add=True, verbose_name='дата оплаты')
    payment_amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    payment_method = models.CharField(choices=PAYMENT_TYPES, default=PAY_CASH,
                                      max_length=100, verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.user} - {self.course if self.course else self.lesson} - {self.date_pay}'

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'оплаты'
