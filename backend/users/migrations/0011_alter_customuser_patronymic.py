# Generated by Django 3.2.16 on 2024-01-11 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_education_year_of_graduation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='patronymic',
            field=models.CharField(blank=True, max_length=150, verbose_name='Отчество'),
        ),
    ]