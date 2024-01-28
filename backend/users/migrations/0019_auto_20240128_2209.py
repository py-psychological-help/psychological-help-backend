# Generated by Django 3.2.16 on 2024-01-28 21:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_auto_20240128_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customclientuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, validators=[django.core.validators.RegexValidator('^[^- ]([а-яА-ЯёЁ -]+)[^- ]+$', 'Разрешены только буквы русского алфавита,\n                               дефис, и символ пробела')], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='customclientuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, validators=[django.core.validators.RegexValidator('^[^- ]([а-яА-ЯёЁ -]+)[^- ]+$', 'Разрешены только буквы русского алфавита,\n                               дефис, и символ пробела')], verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='customclientuser',
            name='patronymic',
            field=models.CharField(blank=True, max_length=50, validators=[django.core.validators.RegexValidator('^[^- ]([а-яА-ЯёЁ -]+)[^- ]+$', 'Разрешены только буквы русского алфавита,\n                               дефис, и символ пробела')], verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[^- ]([а-яА-ЯёЁ -]+)[^- ]+$', 'Разрешены только буквы русского алфавита,\n                               дефис, и символ пробела')], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[^- ]([а-яА-ЯёЁ -]+)[^- ]+$', 'Разрешены только буквы русского алфавита,\n                               дефис, и символ пробела')], verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='patronymic',
            field=models.CharField(blank=True, max_length=50, validators=[django.core.validators.RegexValidator('^[^- ]([а-яА-ЯёЁ -]+)[^- ]+$', 'Разрешены только буквы русского алфавита,\n                               дефис, и символ пробела')], verbose_name='Отчество'),
        ),
    ]
