# Generated by Django 3.2.16 on 2024-02-23 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_chat_is_url_sent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nikname',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nikname', models.CharField(max_length=55, unique=True)),
            ],
        ),
    ]