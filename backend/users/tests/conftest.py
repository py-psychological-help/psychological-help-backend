import pytest
from rest_framework.test import APIClient
from django.core.files.images import ImageFile

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
    return django_user_model.objects.create_user(
        email='p@p.fake',
        password='passssssssss',
        role='psychologist',
        approved_by_moderator=True,
        is_approve_sent=True,
        is_reg_confirm_sent=True,
        first_name='Ivan',
        last_name='Ivanov'
    )


@pytest.fixture()
def psy_auth_user(psy_user):
    """Фикстура `APIClient` с авторизованным пользователем (психологом.)

    Пользователь одобрен модератором.
    """
    psy_client = APIClient()
    psy_client.force_authenticate(psy_user)
    return psy_client


@pytest.fixture()
def document(db, django_user_model, psy_user):
    """Фикстура Документа."""
    image_path = settings.BASE_DIR / 'users' / 'tests' / 'flower.jpg'
    # print(image_path)
    image = open(image_path, 'rb')
    print(image.read())
    # django_image = ImageFile(image)
    # document = Document()
    # document.scan = django_image
    # document.user = psy_user
    # document.save()
    image.close()

    return document
