import pytest
from rest_framework.test import APIClient

try:
    from users.models import CustomClientUser
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружена модель `CustomClientUser` '
        'Она должна находиться в модуле `backend.users.models`'
    )

try:
    from chats.models import Chat
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружена модель `Chat` '
        'Она должна находиться в модуле `backend.chats.models`'
    )

try:
    from chats.models import Message
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружена модель `Message` '
        'Она должна находиться в модуле `backend.chats.models`'
    )


DATETIMEFORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


@pytest.fixture()
def psy_user(db, django_user_model):
    """Фикстура одобренного модератором пользователя (психолога)."""
    return django_user_model.objects.create_user(
        email='p@p.fake',
        password='pass',
        role='psychologist',
        approved_by_moderator=True,
        is_approve_sent=True,
        is_reg_confirm_sent=True,
        first_name='Ivan',
        last_name='Ivanov'
    )


@pytest.fixture()
def psy_client(psy_user):
    """Фикстура `APIClient` с авторизованным пользователем (психологом.)

    Пользователь одобрен модератором.
    """
    psy_client = APIClient()
    psy_client.force_authenticate(psy_user)
    return psy_client


@pytest.fixture()
def customer_user(db):
    """Фикстура пользователя (клиента)."""
    return CustomClientUser.objects.create(
        email='c@c.fake',
        is_reg_confirm_sent=True
    )


@pytest.fixture()
def chat(db, psy_user, customer_user):
    """Фикстура чата."""
    chat = customer_user.client_chats
    chat.psychologist = psy_user
    chat.active = True
    chat.save()
    return chat


@pytest.fixture()
def message(db, chat):
    """Фикстура сообщения."""
    return Message.objects.create(
        text='test_message',
        chat=chat,
        is_psy_author=False
    )


@pytest.fixture()
def psy_without_chat_user(db, django_user_model):
    """Фикстура одобренного модератором пользователя (психолога).

    За пользователем не закреплен чат.
    """
    return django_user_model.objects.create_user(
        email='p2@p.fake',
        password='pass',
        role='psychologist',
        approved_by_moderator=True,
        is_approve_sent=True,
        is_reg_confirm_sent=True
    )


@pytest.fixture()
def psy_without_chat_client(psy_without_chat_user):
    """Фикстура `APIClient` с авторизованным пользователем (психологом.)

    Пользователь одобрен модератором. За пользователем не закреплен чат.
    """
    psy_client = APIClient()
    psy_client.force_authenticate(psy_without_chat_user)
    return psy_client
