# Generated by Django 3.2.16 on 2024-02-09 15:35

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20240209_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customclientuser',
            name='password',
            field=models.CharField(blank=True, max_length=128, validators=[users.validators.PasswordContentValidator, users.validators.PasswordGroupsValidator], verbose_name='password'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(blank=True, max_length=128, validators=[users.validators.PasswordContentValidator, users.validators.PasswordGroupsValidator], verbose_name='password'),
        ),
    ]
