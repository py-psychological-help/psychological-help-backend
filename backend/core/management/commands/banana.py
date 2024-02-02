from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from django.conf import settings

from core.emails import (send_chat_url,)
from core.utils import create_secret_key
from chats.models import Chat
from users.models import Document
from django.core.files.images import ImageFile



User = get_user_model()


class Command(BaseCommand):
    """Команда для тестов и отладки."""

    help = 'Test command.'

    def handle(self, *args, **options):
        psy_user = User.objects.create_user(
            email='p@p.fake11',
            password='passssssssss',
            role='psychologist',
            approved_by_moderator=True,
            is_approve_sent=True,
            is_reg_confirm_sent=True,
            first_name='Ivan',
            last_name='Иванов'
            )

        image_path = settings.BASE_DIR / 'users' / 'tests' / 'flower.jpg'
        with open(image_path, 'rb') as image:
            django_image = ImageFile(image)
            
            document = Document(scan=django_image)
            document.user = psy_user
            document.save()
