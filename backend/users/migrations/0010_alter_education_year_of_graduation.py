# Generated by Django 3.2.16 on 2024-01-11 14:52

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20240111_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='year_of_graduation',
            field=models.IntegerField(blank=True, validators=[users.validators.year_validator], verbose_name='Год окончания'),
        ),
    ]
