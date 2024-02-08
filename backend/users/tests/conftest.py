import pytest
from rest_framework.test import APIClient
from django.core.files.images import ImageFile
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from pathlib import Path


try:
    from users.models import CustomClientUser
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружена модель `CustomClientUser` '
        'Она должна находиться в модуле `backend.users.models`'
    )

try:
    from users.models import CustomClientUser
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружена модель `CustomClientUser` '
        'Она должна находиться в модуле `backend.users.models`'
    )

try:
    from users.models import Document
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружена модель `Document` '
        'Она должна находиться в модуле `backend.users.models`'
    )

from django.conf import settings
from django.core.files.base import ContentFile


@pytest.fixture()
def psy_user(db, django_user_model):
    """Фикстура одобренного модератором пользователя (психолога)."""
    image_path = str(settings.BASE_DIR / 'users' / 'tests' / 'flower.jpg')
    return django_user_model.objects.create_user(
        email='p@p.fake',
        password='passssssssss',
        role='psychologist',
        approved_by_moderator=True,
        is_approve_sent=True,
        is_reg_confirm_sent=True,
        first_name='Ivan',
        last_name='Ivanov',
        photo=image_path
    )


@pytest.fixture()
def psy_moderator(db, django_user_model):
    """Фикстура одобренного модератором пользователя (психолога)."""
    image_path = str(settings.BASE_DIR / 'users' / 'tests' / 'flower.jpg')
    return django_user_model.objects.create_user(
        email='p@p.fake',
        password='passssssssss',
        role='moderator',
        approved_by_moderator=True,
        is_approve_sent=True,
        is_reg_confirm_sent=True,
        first_name='Ivan',
        last_name='Ivanov',
        photo=image_path
    )


@pytest.fixture()
def psy_not_auth_user(psy_user):
    """Фикстура `APIClient` с неавторизованным пользователем (психологом.)

    Пользователь одобрен модератором.
    """
    psy_client = APIClient()
    return psy_client


@pytest.fixture()
def psy_auth_user(psy_user):
    """Фикстура `APIClient` с авторизованным пользователем (психологом.)

    Пользователь одобрен модератором.
    """
    psy_client = APIClient()
    psy_client.force_authenticate(psy_user)
    return psy_client


@pytest.fixture()
def psy_auth_moderator_user(psy_moderator):
    """Фикстура `APIClient` с авторизованным пользователем (модератор.)

    """
    psy_client = APIClient()
    psy_client.force_authenticate(psy_moderator)
    return psy_client


@pytest.fixture()
def document(db, django_user_model, psy_user):
    """Фикстура Документа."""
    image_path = 'scans/' + 'flower.jpg'
    return Document.objects.create(
        user=psy_user,
        name='test_document',
        scan=image_path
    )
