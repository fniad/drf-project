from django.core.management import BaseCommand
from django.core.management import call_command
from payment.models import Payment
from training_courses.models import Course, Lesson


class Command(BaseCommand):
    help = 'Удалить все объекты из БД.'

    def handle(self, *args, **options):
        Payment.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()

        call_command('loaddata', 'fixtures/data.json')

        self.stdout.write(self.style.SUCCESS('Объекты были добавлены в БД'))
