import pytest
from rest_framework.test import APIClient
from django.core.exceptions import FieldDoesNotExist
from users.models import CustomUser, CustomClientUser, Document
# from users.tests.conftest import document
from http import HTTPStatus
from rest_framework import status
from django.contrib.auth import get_user_model



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

# нужно запретить
@pytest.mark.xfail
def test_auth_user_reg(psy_auth_user):
    url = f'/api/v1/users/psychologists/'
    response = psy_auth_user.post(url,
                                  {
    "email": "lkjasfnd424@mail.ru",
    "first_name": "ФродБэггинс",
    "last_name": "вафыавыф",
    "password": "Ss12345!",
    "birth_date": "2000-05-01"
})
    assert response.status_code == status.HTTP_403_FORBIDDEN


# нужно запретить
@pytest.mark.xfail
def test_auth_user_reg_client(psy_auth_user):
    url = f'/api/v1/users/psychologists/'
    response = psy_auth_user.post(url,
                                  {
    "email": "u1ser@example.com",
    "complaint": "Обязательное поле."
})
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_anon_user_reg(psy_not_auth_user):
    url = f'/api/v1/users/psychologists/'
    User = get_user_model()
    user_count = User.objects.count()
    response = psy_not_auth_user.post(url,
                                  {
    "email": "lkjasfnd424@mail.ru",
    "first_name": "ФродБэггинс",
    "last_name": "вафыавыф",
    "password": "Ss12345!",
    "birth_date": "2000-05-01"
})
    assert user_count + 1 == User.objects.count()
    assert response.status_code == status.HTTP_201_CREATED


def test_anon_client_reg(psy_not_auth_user):
    url = f'/api/v1/users/clients/'
    client_count = CustomClientUser.objects.count()
    response = psy_not_auth_user.post(url,
                                      {
    "email": "u1ser@example.com",
    "complaint": "Обязательное поле."
})
    assert client_count + 1 == CustomClientUser.objects.count()
    assert response.status_code == status.HTTP_201_CREATED


def test_auth_user_add_doc(psy_auth_user):
    url = f'/api/v1/users/psychologists/me/documents/'
    docs_count = Document.objects.count()
    response = psy_auth_user.post(url,
                                      {
    "scan": "data:image/jpeg;base64,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"
})
    assert docs_count + 1 == Document.objects.count()
    assert response.status_code == status.HTTP_201_CREATED