# Generated by Django 3.2.16 on 2024-01-14 15:40

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_education_year_of_graduation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='year_of_graduation',
            field=models.IntegerField(blank=True, null=True, validators=[users.validators.year_validator], verbose_name='Год окончания'),
        ),
    ]