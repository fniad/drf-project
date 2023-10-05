from django.core import serializers
from django.core.management import BaseCommand
from itertools import chain

from payment.models import Payment


class Command(BaseCommand):
    help = 'Перенос БД в json-файл'

    def handle(self, *args, **options):
        models = [Payment]

        with open('fixtures/data.json', 'w') as file:
            data = serializers.serialize('json', chain(*[model.objects.all() for model in models]))
            file.write(data)

        self.stdout.write(self.style.SUCCESS('Данные по оплатам из БД успешно сохранены в data.json'))
