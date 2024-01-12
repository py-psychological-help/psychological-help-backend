# Generated by Django 3.2.16 on 2024-01-11 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20240110_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='customclientuser',
            name='password',
            field=models.CharField(blank=True, max_length=128, verbose_name='password'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Администратор'), ('moderator', 'Модератор'), ('psychologist', 'Психолог')], default='PSYCHOLOGIST', max_length=25),
        ),
    ]