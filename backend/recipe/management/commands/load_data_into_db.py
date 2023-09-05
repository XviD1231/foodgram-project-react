import csv
from django.core.management.base import BaseCommand
from ingredients.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка ингридиентов из CSV файла.'

    def add_arguments(self, parser):
        parser.add_argument('--csv_path', type=str,
                            help='Путь к CSV файлу с ингредиентами')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_path']
        self.load_ingredients_from_csv(csv_file)

    def load_ingredients_from_csv(self, file_path):
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                if len(row) == 2:
                    name = row[0]
                    measurement_unit = row[1]
                    Ingredient.objects.create(
                        name=name,
                        measurement_unit=measurement_unit
                    )
                    self.stdout.write(self.style.SUCCESS(
                        f'Успешно добавлен в БД ингредиент: {name}')
                        )
