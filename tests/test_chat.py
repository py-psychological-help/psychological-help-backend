from http import HTTPStatus

import pytest
from django.core.exceptions import FieldDoesNotExist
from rest_framework.test import APIClient

from tests.conftest import DATETIMEFORMAT, Chat, CustomClientUser


@pytest.fixture()
def psy_not_approved_client(db, django_user_model):
    """Фикстура `APIClient` с авторизованным пользователем (психологом.)

    Пользователь не одобрен модератором.
    """
    user = django_user_model.objects.create_user(
        email='p@p.fake',
        password='pass',
        role='psychologist',
        approved_by_moderator=False,
        is_approve_sent=True,
        is_reg_confirm_sent=True
    )
    psy_client = APIClient()
    psy_client.force_authenticate(user)
    return psy_client


@pytest.fixture()
def chat_without_psychologist(db):
    """Фикстура чата без закрепленного психолога."""
    customer_user = CustomClientUser.objects.create(
        email='c2@c.fake',
        is_reg_confirm_sent=True
    )
    chat = customer_user.client_chats
    return chat


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
        'field',
        ['client', 'psychologist', 'date_time', 'active', 'chat_secret_key'])
def test_chat_model_fields(field):
    try:
        Chat._meta.get_field(field)
    except FieldDoesNotExist:
        assert False, (
            f'Убедитесь, что у модели `Chat` имеется поле `{field}`'
        )


@pytest.mark.parametrize(
    'test_client, expected, notification',
    [
        ('psy_client',
         HTTPStatus.OK,
         ('GET-запрос подтвержденного и авторизованного пользователя '
          'к `{}` должен возвращать ответ со статусом 200')),
        ('psy_not_approved_client',
         HTTPStatus.FORBIDDEN,
         ('GET-запрос авторизованного, но не подтвержденного пользователя '
          'к `{}` должен возвращать ответ со статусом 403')),
        ('client',
         HTTPStatus.UNAUTHORIZED,
         ('GET-запрос не авторизованного пользователя '
          'к `{}` должен возвращать ответ со статусом 401')),

    ]
)
def test_chats_list_status(request, test_client, expected, notification):
    url = '/api/v1/chats/'
    test_client = request.getfixturevalue(test_client)
    response = test_client.get(url)
    assert response.status_code == expected, notification.format(url)


def test_chats_list_data(psy_client, psy_user, customer_user, chat, message):
    url = '/api/v1/chats/'
    response = psy_client.get(url)
    expected_data = [
        {
            'id': chat.id,
            'chat_secret_key': chat.chat_secret_key,
            'active': chat.active,
            'new': False,
            'client': {
                'id': customer_user.id,
                'email': customer_user.email,
                'first_name': customer_user.first_name,
                'complaint': customer_user.complaint
            },
            'psychologist': {
                'first_name': psy_user.first_name,
                'last_name': psy_user.last_name,
                'birth_date': psy_user.birth_date,
                'photo': None,
                'greeting': psy_user.greeting
            },
            'messages': [{
                'id': message.id,
                'text': message.text,
                'date_time': message.date_time.strftime(DATETIMEFORMAT),
                'is_author_me': False,
                'author': customer_user.id,
            },]
        }
    ]
    assert response.json() == expected_data, (
        f'Убедитесь, что GET-запрос к `{url}` возвращает корректные данные'
    )


def test_chat_retrieve_data(
    psy_client, psy_user, customer_user, chat, message
):
    url = f'/api/v1/chats/{chat.chat_secret_key}/'
    response = psy_client.get(url)
    expected_data = {
        'id': chat.id,
        'chat_secret_key': chat.chat_secret_key,
        'active': chat.active,
        'new': False,
        'client': {
            'id': customer_user.id,
            'email': customer_user.email,
            'first_name': customer_user.first_name,
            'complaint': customer_user.complaint
        },
        'psychologist': {
            'first_name': psy_user.first_name,
            'last_name': psy_user.last_name,
            'birth_date': psy_user.birth_date,
            'photo': None,
            'greeting': psy_user.greeting
        },
        'messages': [{
            'id': message.id,
            'text': message.text,
            'date_time': message.date_time.strftime(DATETIMEFORMAT),
            'is_author_me': False,
            'author': customer_user.id,
        },]
    }
    assert response.json() == expected_data, (
        f'Убедитесь, что GET-запрос к `{url}` возвращает корректные данные'
    )


def test_chat_delete_status(psy_client, chat):
    url = f'/api/v1/chats/{chat.chat_secret_key}/'
    response = psy_client.delete(url)
    assert response.status_code == HTTPStatus.NO_CONTENT, (
        f'DELETE-запрос к `{url}` должен возвращать ответ со статусом 204'
    )


def test_chat_delete_content(psy_client, chat):
    url = f'/api/v1/chats/{chat.chat_secret_key}/'
    before_count = Chat.objects.count()
    psy_client.delete(url)
    after_count = Chat.objects.count()
    chat_exists = Chat.objects.filter(id=chat.id).exists()
    assert after_count == before_count - 1 and not chat_exists, (
        f'Убедитесь, что DELETE-запрос к `{url}` удаляет чат.'
    )


@pytest.mark.parametrize(
    'test_client, expected, notification',
    [
        ('psy_without_chat_client',
         HTTPStatus.CREATED,
         ('POST-запрос авторизованного пользователя к `{}` '
          'должен возвращать ответ со статусом 201')),
        ('client',
         HTTPStatus.UNAUTHORIZED,
         ('POST-запрос не авторизованного пользователя к `{}` '
          'должен возвращать ответ со статусом 401')),

    ]
)
def test_chat_start_status(
    request, test_client, expected, notification, chat_without_psychologist
):
    url = f'/api/v1/chats/{chat_without_psychologist.chat_secret_key}/start/'
    test_client = request.getfixturevalue(test_client)
    response = test_client.post(url)
    assert response.status_code == expected, notification.format(url)


def test_chat_start_data(
    psy_without_chat_user, psy_without_chat_client, chat_without_psychologist
):
    url = f'/api/v1/chats/{chat_without_psychologist.chat_secret_key}/start/'
    psy_without_chat_client.post(url)
    chat_without_psychologist.refresh_from_db()
    assert chat_without_psychologist.psychologist == psy_without_chat_user, (
        'Убедитесь, что в результате POST-запроса авторизованного '
        f'пользователя к `{url}` за указанным чатом закрепляется психолог '
        '(то есть поле `psychologist` соответствующего объекта модели `Chat` '
        'начинает ссылаться на сделавшего запрос пользователя)'
    )


def test_chat_start_already_active(psy_without_chat_client, chat):
    url = f'/api/v1/chats/{chat.chat_secret_key}/start/'
    response = psy_without_chat_client.post(url)
    assert response.status_code == HTTPStatus.BAD_REQUEST, (
        'Убедитесь, что POST-запрос авторизованного пользователя '
        f'к `{url}` возвращает статус 400, если за указанным '
        'чатом уже закреплен психолог'
    )


@pytest.mark.parametrize(
    'test_client, expected, notification',
    [
        ('psy_client',
         HTTPStatus.CREATED,
         ('POST-запрос авторизованного пользователя к `{}` '
          'должен возвращать ответ со статусом 201, '
          'если за этим пользователем закреплен указанный в url чат')),
        ('psy_without_chat_client',
         HTTPStatus.FORBIDDEN,
         ('POST-запрос авторизованного пользователя к `{}` '
          'должен возвращать ответ со статусом 403, '
          'если за этим пользователем не закреплен указанный в url чат')),
        ('client',
         HTTPStatus.UNAUTHORIZED,
         ('POST-запрос не авторизованного пользователя к `{}` '
          'должен возвращать ответ со статусом 401')),

    ]
)
def test_chat_finish_status(
    request, test_client, expected, notification, chat
):
    url = f'/api/v1/chats/{chat.chat_secret_key}/finish/'
    test_client = request.getfixturevalue(test_client)
    response = test_client.post(url)
    assert response.status_code == expected, notification.format(url)


def test_chat_finish_data(psy_client, chat):
    url = f'/api/v1/chats/{chat.chat_secret_key}/finish/'
    psy_client.post(url)
    chat.refresh_from_db()
    assert not chat.active, (
        'Убедитесь, что в результате POST-запроса закрепленного за чатом '
        f'авторизованного пользователя к `{url}` указанный чат становится '
        'неактивным (то есть поле `active` соответствующего объекта модели '
        '`Chat` изменяется на значение `False`)'
    )


@pytest.mark.parametrize('url', ['/api/v1/chats/unexisting_key/'])
def test_get_404_chat_url(psy_client, url):
    response = psy_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'GET-запрос к `{url}` с отсутствующим чатом должен '
        'возвращать ответ со статусом 404'
    )


@pytest.mark.parametrize('url', ['/api/v1/chats/unexistingkey/'])
def test_delete_404_chat_url(psy_client, url):
    response = psy_client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'DELETE-запрос к `{url}` с отсутствующим чатом должен '
        'возвращать ответ со статусом 404'
    )


@pytest.mark.parametrize(
    'url',
    [
        '/api/v1/chats/unexistingkey/start/',
        '/api/v1/chats/unexistingkey/finish/',

    ]
)
def test_post_404_chat_url(psy_client, url):
    response = psy_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'POST-запрос к `{url}` с отсутствующим чатом должен '
        'возвращать ответ со статусом 404'
    )
