# Generated by Django 3.2.16 on 2024-01-12 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customclientuser_complaint_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customclientuser',
            old_name='complaint_text',
            new_name='complaint',
        ),
    ]
