# Generated by Django 3.2.16 on 2024-01-13 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_complaint_text_customclientuser_complaint'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='greeting',
            field=models.TextField(blank=True),
        ),
    ]