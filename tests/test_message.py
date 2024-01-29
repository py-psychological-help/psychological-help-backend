from http import HTTPStatus

import pytest
from django.core.exceptions import FieldDoesNotExist
from rest_framework.test import APIClient

from tests.conftest import DATETIMEFORMAT, Message

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
        'field',
        ['text', 'date_time', 'chat', 'is_psy_author'])
def test_chat_model_fields(field):
    try:
        Message._meta.get_field(field)
    except FieldDoesNotExist:
        assert False, (
            f'Убедитесь, что у модели `Message` имеется поле `{field}`'
        )


def test_messages_get_status(psy_client, chat):
    url = f'/api/v1/chats/{chat.chat_secret_key}/messages/'
    response = psy_client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        'GET-запрос к `{url}` должен возвращать ответ со статусом 200'
    )


def test_messages_data(psy_client, chat, message):
    url = f'/api/v1/chats/{chat.chat_secret_key}/messages/'
    response = psy_client.get(url)
    expected_data = [
        {
            'id': message.id,
            'text': message.text,
            'date_time': message.date_time.strftime(DATETIMEFORMAT),
            'is_author_me': False,
            'author': chat.client.id
        }
    ]
    assert response.json() == expected_data, (
        f'Убедитесь, что GET-запрос к `{url}` возвращает корректные данные'
    )


@pytest.mark.parametrize(
    'test_client, expected, notification',
    [
        ('psy_client',
         HTTPStatus.CREATED,
         ('POST-запрос авторизованного пользователя к `{}` должен возвращать '
          'ответ со статусом 201, если чат по указанному `url '
          'закреплен за этим пользователем')),
        ('client',
         HTTPStatus.CREATED,
         ('POST-запрос неавторизованного пользователя к `{}` должен '
          'возвращать ответ со статусом 201')),
        ('psy_without_chat_client',
         HTTPStatus.FORBIDDEN,
         ('POST-запрос авторизованного пользователя к `{}` должен возвращать '
          'ответ со статусом 403, если чат по указанному `url '
          'не закреплен за этим пользователем')),

    ]
)
def test_messages_post_status(
    request, test_client, expected, notification, chat
):
    url = f'/api/v1/chats/{chat.chat_secret_key}/messages/'
    test_client = request.getfixturevalue(test_client)
    data = {
        'text': 'some_text'
    }
    response = test_client.post(url, data)
    assert response.status_code == expected, notification


def test_message_post_data(psy_client, chat):
    url = f'/api/v1/chats/{chat.chat_secret_key}/messages/'
    text = 'some_text'
    data = {
        'text': text
    }
    response = psy_client.post(url, data)
    assert response.json().get('text') == text, (
        f'Убедитесь, что POST-запрос к `{url}` возвращает в ответе '
        'переданное в теле запроса значение поля `text`'
    )


def test_message_author_psychologist(psy_user, psy_client, chat):
    url = f'/api/v1/chats/{chat.chat_secret_key}/messages/'
    data = {
        'text': 'some_text'
    }
    response = psy_client.post(url, data)
    assert response.json().get('author') == psy_user.id, (
        f'Убедитесь, что POST-запрос авторизованного пользователя к `{url}` '
        'возвращает в ответе в поле `author` `id` пользователя'
    )
    assert response.json().get('is_author_me'), (
        f'Убедитесь, что POST-запрос авторизованного пользователя к `{url}` '
        'возвращает в ответе в поле `is_author_me` значение `True`'
    )


def test_message_author_customer(client, chat):
    url = f'/api/v1/chats/{chat.chat_secret_key}/messages/'
    data = {
        'text': 'some_text'
    }
    response = client.post(url, data)
    assert response.json().get('author') == chat.client.id, (
        'Убедитесь, что POST-запрос не авторизованного пользователя '
        f'к `{url}` возвращает в ответе в поле `author` `id` '
        'пользователя (клиента), привязанного к чату'
    )
    assert response.json().get('is_author_me'), (
        'Убедитесь, что POST-запрос не авторизованного пользователя '
        f'к `{url}` возвращает в ответе в поле `is_author_me` значение `True`'
    )


@pytest.mark.parametrize(
        'test_client, expected, notification',
        [
            ('psy_client',
             True,
             'Убедитесь, что при создании сообщения авторизованным '
             'пользователем (психологом) в поле `is_psy_author` '
             'нового объекта модели `Message` установлено значение `True`'),
            ('client',
             False,
             'Убедитесь, что при создании сообщения не авторизованным '
             'пользователем (клиентом) в поле `is_psy_author` '
             'нового объекта модели `Message` установлено значение `False`')
        ]
)
def test_message_is_psy_author_field(
    request, test_client, expected, notification, chat
):
    url = f'/api/v1/chats/{chat.chat_secret_key}/messages/'
    test_client = request.getfixturevalue(test_client)
    text = 'text_for_is_psy_author_check'
    data = {
        'text': text
    }
    test_client.post(url, data)
    message = Message.objects.filter(text=text).first()
    assert message, (
        f'Убедитесь, что при POST-запросе к `{url}` создается '
        'новый объект модели `Message`'
    )
    assert message.is_psy_author == expected, notification


@pytest.mark.parametrize('text', ['', None, [], {}, True])
def test_message_bad_data(psy_client, chat, text):
    url = f'/api/v1/chats/{chat.chat_secret_key}/messages/'
    data = {
        'text': text
    }
    response = psy_client.post(url, data, content_type='application/json')
    assert response.status_code == HTTPStatus.BAD_REQUEST, (
        f'Убедитесь, что POST-запрос к `{url}` с не валидными данными '
        'возвращает статус 400'
    )


def test_message_no_data(psy_client, chat):
    url = f'/api/v1/chats/{chat.chat_secret_key}/messages/'
    response = psy_client.post(url)
    assert response.status_code == HTTPStatus.BAD_REQUEST, (
        f'Убедитесь, что POST-запрос к `{url}` без данных в теле запроса '
        'возвращает статус 400'
    )


def test_get_404_chat_url(psy_client, chat):
    url = '/api/v1/chats/unexistingkey/messages/'
    response = psy_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        f'GET-запрос к `{url}` с отсутствующим чатом должен '
        'возвращать ответ со статусом 404'
    )


def test_post_404_chat_url(psy_client, chat):
    url = '/api/v1/chats/unexistingkey/messages/'
    data = {
        'text': 'some_text'
    }
    response = psy_client.post(url, data)
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        f'POST-запрос к `{url}` с отсутствующим чатом должен '
        'возвращать ответ со статусом 404'
    )
