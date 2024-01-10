import json
import os
from io import open

from django.core.management.base import BaseCommand

from recipes.models import Ingredient as Ingrt


def ingredient_import_json():
    """Импорт объектов ингредиентов из json-файла."""
    os.chdir('..')
    os.chdir('data')
    full_path = os.getcwd()
    with open(full_path + r'/ingredients.json',
              encoding='utf-8') as f:
        data = json.load(f)
        for object in data:

            try:
                name = object["name"]
                mu = object["measurement_unit"]
                ingredient = Ingrt.objects.get_or_create(name=name,
                                                         measurement_unit=mu)
                print(f'Объект импортирован: {ingredient},')

            except SystemError:
                print('Ошибка импортирования')


class Command(BaseCommand):
    """Импорт ингредиентов."""

    help = 'Command to import ingredients'

    def handle(self, *args, **options):
        ingredient_import_json()
