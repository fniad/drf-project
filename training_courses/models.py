from django.db import models

from users.models import NULLABLE


class Course(models.Model):
    name_course = models.CharField(max_length=100, verbose_name='название курса')
    preview_img_course = models.ImageField(upload_to='courses/', verbose_name='превью курса', **NULLABLE)
    description_course = models.TextField(verbose_name='описание курса')

    def __str__(self):
        return f'{self.name_course}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name_lesson = models.CharField(max_length=100, verbose_name='название урока')
    description_lesson = models.TextField(verbose_name='описание урока')
    preview_img_lesson = models.ImageField(upload_to='lessons/', **NULLABLE, verbose_name='превью урока')
    video_url_lesson = models.TextField(**NULLABLE, verbose_name='url_видео')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='курс')

    def __str__(self):
        return f'{self.name_lesson}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
