# Generated by Django 3.2.16 on 2024-01-29 18:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20240129_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customclientuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, validators=[django.core.validators.RegexValidator('^[a-z0-9_.-]+@[a-z0-9.-]+\\.[a-zA-Z]{2,}$', 'Разрешены только строчные буквы латинского алфавита, цифры, и символы “@”, “-”, “_” и “.”. '), django.core.validators.RegexValidator('^(?!.*\\.\\-)(?!.*\\-\\.)(?!.*\\_\\.)(?!.*\\.\\_)(?!.*\\.\\.)', 'Запрещено использование двойных точек, специальных символов, а так же комбинаций точки с тире и символом нижнего подчеркивания')], verbose_name='email адрес'),
        ),
        migrations.AlterField(
            model_name='customclientuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, validators=[django.core.validators.RegexValidator('^(?!.*\\s{2})(?!.*\\-{2})', 'Двойные дефисы и пробелы запрещены'), django.core.validators.RegexValidator('^[^- ][а-яА-ЯёЁ\\s-]+[^- ]$', 'Разрешены только буквы русского алфавита, дефис, и символ пробела. Дефисы и пробелы не могут находиться в начале и в конце ввода')], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='customclientuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, validators=[django.core.validators.RegexValidator('^(?!.*\\s{2})(?!.*\\-{2})', 'Двойные дефисы и пробелы запрещены'), django.core.validators.RegexValidator('^[^- ][а-яА-ЯёЁ\\s-]+[^- ]$', 'Разрешены только буквы русского алфавита, дефис, и символ пробела. Дефисы и пробелы не могут находиться в начале и в конце ввода')], verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='customclientuser',
            name='password',
            field=models.CharField(blank=True, max_length=20, verbose_name='password'),
        ),
        migrations.AlterField(
            model_name='customclientuser',
            name='patronymic',
            field=models.CharField(blank=True, max_length=50, validators=[django.core.validators.RegexValidator('^(?!.*\\s{2})(?!.*\\-{2})', 'Двойные дефисы и пробелы запрещены'), django.core.validators.RegexValidator('^[^- ][а-яА-ЯёЁ\\s-]+[^- ]$', 'Разрешены только буквы русского алфавита, дефис, и символ пробела. Дефисы и пробелы не могут находиться в начале и в конце ввода')], verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^[a-z0-9_.-]+@[a-z0-9.-]+\\.[a-zA-Z]{2,}$', 'Разрешены только строчные буквы латинского алфавита, цифры, и символы “@”, “-”, “_” и “.”. '), django.core.validators.RegexValidator('^(?!.*\\.\\-)(?!.*\\-\\.)(?!.*\\_\\.)(?!.*\\.\\_)(?!.*\\.\\.)', 'Запрещено использование двойных точек, специальных символов, а так же комбинаций точки с тире и символом нижнего подчеркивания')], verbose_name='email адрес'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^(?!.*\\s{2})(?!.*\\-{2})', 'Двойные дефисы и пробелы запрещены'), django.core.validators.RegexValidator('^[^- ][а-яА-ЯёЁ\\s-]+[^- ]$', 'Разрешены только буквы русского алфавита, дефис, и символ пробела. Дефисы и пробелы не могут находиться в начале и в конце ввода')], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^(?!.*\\s{2})(?!.*\\-{2})', 'Двойные дефисы и пробелы запрещены'), django.core.validators.RegexValidator('^[^- ][а-яА-ЯёЁ\\s-]+[^- ]$', 'Разрешены только буквы русского алфавита, дефис, и символ пробела. Дефисы и пробелы не могут находиться в начале и в конце ввода')], verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='patronymic',
            field=models.CharField(blank=True, max_length=50, validators=[django.core.validators.RegexValidator('^(?!.*\\s{2})(?!.*\\-{2})', 'Двойные дефисы и пробелы запрещены'), django.core.validators.RegexValidator('^[^- ][а-яА-ЯёЁ\\s-]+[^- ]$', 'Разрешены только буквы русского алфавита, дефис, и символ пробела. Дефисы и пробелы не могут находиться в начале и в конце ввода')], verbose_name='Отчество'),
        ),
    ]
