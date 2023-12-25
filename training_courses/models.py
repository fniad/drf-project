""" Модели приложения training_courses """
from django.db import models
from users.models import NULLABLE, User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Course(models.Model):
    """ Модель курса """
    name_course = models.CharField(max_length=100, verbose_name='название курса')
    preview_img_course = models.ImageField(upload_to='courses/', verbose_name='превью курса', **NULLABLE)
    description_course = models.TextField(verbose_name='описание курса')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, verbose_name='Владелец')
    price = models.PositiveIntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)

    @property
    def display_price(self) -> str:
        return '${0:.2f}'.format(self.price)

    @property
    def stripe_price_data(self) -> dict:
        return {
            'currency': 'usd',
            'unit_amount': self.price,
            'product_data': {
                'name': self.name_course,
            },
        }


    def __str__(self):
        return f'{self.name_course}'

    class Meta:
        """ Мета-данные """
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    """ Модель урока """
    name_lesson = models.CharField(max_length=100, verbose_name='название урока')
    description_lesson = models.TextField(verbose_name='описание урока')
    preview_img_lesson = models.ImageField(upload_to='lessons/', **NULLABLE, verbose_name='превью урока')
    video_url_lesson = models.URLField(**NULLABLE, verbose_name='url_видео')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='курс')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Владелец')
    price = models.PositiveIntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)

    @property
    def display_price(self) -> str:
        return '${0:.2f}'.format(self.price)

    @property
    def stripe_price_data(self) -> dict:
        return {
            'currency': 'usd',
            'unit_amount': self.price,
            'product_data': {
                'name': self.name_lesson,
            },
        }


    def __str__(self):
        return f'{self.name_lesson}'

    class Meta:
        """ Мета-данные """
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


# Добавляем обработчик сигнала
@receiver(post_save, sender=Lesson)
def update_course_on_lesson_save(sender, instance, **kwargs):
    """ Обработчик сигнала при сохранении урока или обновлении, обновляет связанный с уроком курс """
    if instance.course:  # Проверяем, что урок связан с конкретным курсом
        course = instance.course
        course.last_update = instance.last_update
        course.save()


class Subscription(models.Model):
    """ Модель подписки """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, related_name='subscription')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE, related_name='subscription')
    is_active = models.BooleanField(verbose_name='активность', default=False)

    def __str__(self):
        return f'{self.user} - {self.course if self.course else self.lesson} - {self.is_active}'

    class Meta:
        """ Мета-данные """
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
