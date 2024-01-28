# Generated by Django 3.2.16 on 2024-01-28 21:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_auto_20240128_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customclientuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, validators=[django.core.validators.RegexValidator('^(?!.*\\s{2})(?!.*\\-{2})', 'Двойные дефисы и пробелы запрещены'), django.core.validators.RegexValidator('^[^- ][а-яА-ЯёЁ\\s-]+[^- ]$', 'Разрешены только буквы русского\n                                      алфавита, дефис, и символ пробела.\n                                      Дефисы и пробелы не могут находиться\n                                      в начале и в конце')], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='customclientuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, validators=[django.core.validators.RegexValidator('^(?!.*\\s{2})(?!.*\\-{2})', 'Двойные дефисы и пробелы запрещены'), django.core.validators.RegexValidator('^[^- ][а-яА-ЯёЁ\\s-]+[^- ]$', 'Разрешены только буквы русского\n                                      алфавита, дефис, и символ пробела.\n                                      Дефисы и пробелы не могут находиться\n                                      в начале и в конце')], verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='customclientuser',
            name='patronymic',
            field=models.CharField(blank=True, max_length=50, validators=[django.core.validators.RegexValidator('^(?!.*\\s{2})(?!.*\\-{2})', 'Двойные дефисы и пробелы запрещены'), django.core.validators.RegexValidator('^[^- ][а-яА-ЯёЁ\\s-]+[^- ]$', 'Разрешены только буквы русского\n                                      алфавита, дефис, и символ пробела.\n                                      Дефисы и пробелы не могут находиться\n                                      в начале и в конце')], verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^(?!.*\\s{2})(?!.*\\-{2})', 'Двойные дефисы и пробелы запрещены'), django.core.validators.RegexValidator('^[^- ][а-яА-ЯёЁ\\s-]+[^- ]$', 'Разрешены только буквы русского\n                                      алфавита, дефис, и символ пробела.\n                                      Дефисы и пробелы не могут находиться\n                                      в начале и в конце')], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^(?!.*\\s{2})(?!.*\\-{2})', 'Двойные дефисы и пробелы запрещены'), django.core.validators.RegexValidator('^[^- ][а-яА-ЯёЁ\\s-]+[^- ]$', 'Разрешены только буквы русского\n                                      алфавита, дефис, и символ пробела.\n                                      Дефисы и пробелы не могут находиться\n                                      в начале и в конце')], verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='patronymic',
            field=models.CharField(blank=True, max_length=50, validators=[django.core.validators.RegexValidator('^(?!.*\\s{2})(?!.*\\-{2})', 'Двойные дефисы и пробелы запрещены'), django.core.validators.RegexValidator('^[^- ][а-яА-ЯёЁ\\s-]+[^- ]$', 'Разрешены только буквы русского\n                                      алфавита, дефис, и символ пробела.\n                                      Дефисы и пробелы не могут находиться\n                                      в начале и в конце')], verbose_name='Отчество'),
        ),
    ]
