import pytest
from rest_framework.test import APIClient
from django.core.exceptions import FieldDoesNotExist

from users.models import CustomUser, CustomClientUser, Document
from users.tests.conftest import document
from http import HTTPStatus
from rest_framework import status



@pytest.mark.parametrize(
        'field',
        ['name', 'scan', ])
def test_document_fields(field):
    try:
        Document._meta.get_field(field)
    except FieldDoesNotExist:
        assert False, (
                f'Убедитесь, что у модели `Document` имеется поле `{field}`'
            )

@pytest.mark.parametrize(
    'test_client, expected, notification',
    [
        ('psy_auth_user',
         status.HTTP_200_OK,
         ('GET-запрос подтвержденного и авторизованного пользователя '
          'к `{}` должен возвращать ответ со статусом 200')),
        ('psy_not_auth_user',
         status.HTTP_401_UNAUTHORIZED,
         ('GET-запрос не авторизованного пользователя '
          'к `{}` должен возвращать ответ со статусом 401')),

    ]
)
def test_me_page_status(request, test_client, expected, notification):
    url = '/api/v1/users/psychologists/me/'
    test_client = request.getfixturevalue(test_client)
    response = test_client.get(url)
    assert response.status_code == expected


@pytest.mark.parametrize(
    'test_client, expected, notification',
    [
        ('psy_auth_user',
         status.HTTP_200_OK,
         ('GET-запрос подтвержденного и авторизованного пользователя '
          'к `{}` должен возвращать ответ со статусом 200')),
        ('psy_not_auth_user',
         status.HTTP_401_UNAUTHORIZED,
         ('GET-запрос не авторизованного пользователя '
          'к `{}` должен возвращать ответ со статусом 401')),

    ]
)
def test_me_docs_status(request, test_client, expected, notification):
    url = '/api/v1/users/psychologists/me/documents/'
    test_client = request.getfixturevalue(test_client)
    response = test_client.get(url)
    assert response.status_code == expected


@pytest.mark.parametrize(
    'test_client, expected, notification',
    [
        ('psy_auth_moderator_user',
         status.HTTP_200_OK,
         ('GET-запрос подтвержденного и авторизованного пользователя '
          'к `{}` должен возвращать ответ со статусом 200')),
        ('psy_not_auth_user',
         status.HTTP_401_UNAUTHORIZED,
         ('GET-запрос не авторизованного пользователя '
          'к `{}` должен возвращать ответ со статусом 401')),
        ('psy_auth_user',
         status.HTTP_403_FORBIDDEN,
         ('GET-запрос не модератора '
          'к `{}` должен возвращать ответ со статусом 403')),

    ]
)
def test_psy_list_status(request, test_client, expected, notification):
    url = '/api/v1/users/psychologists/'
    test_client = request.getfixturevalue(test_client)
    response = test_client.get(url)
    assert response.status_code == expected, notification.format(url)


@pytest.mark.parametrize(
    'test_client, test_user, expected, notification',
    [
        ('psy_auth_moderator_user',
         'psy_moderator',
         status.HTTP_200_OK,
         ('GET-запрос подтвержденного и авторизованного пользователя '
          'к `{}` должен возвращать ответ со статусом 200')),
        ('psy_not_auth_user',
         'psy_user',
         status.HTTP_401_UNAUTHORIZED,
         ('GET-запрос не авторизованного пользователя '
          'к `{}` должен возвращать ответ со статусом 401')),
        #   потенциально опасно давать любым юзерам давать доступ ко всей инфе
        #   любого пользователя по id
        # ('psy_auth_user',
        #  'psy_user',
        #  status.HTTP_403_FORBIDDEN,
        #  ('GET-запрос не модератора '
        #   'к `{}` должен возвращать ответ со статусом 403')),

    ]
)
def test_psy_page_status(request, test_client, test_user, expected, notification):
    test_user = request.getfixturevalue(test_user)
    url = f'/api/v1/users/psychologists/{test_user.id}/'
    test_client = request.getfixturevalue(test_client)
    response = test_client.get(url)
    assert response.status_code == expected, notification.format(url)
