# Generated by Django 3.2.16 on 2024-01-13 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20240113_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customclientuser',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
