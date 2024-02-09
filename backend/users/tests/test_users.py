import pytest

from users.models import CustomClientUser
from rest_framework import status
from django.contrib.auth import get_user_model


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


def test_psy_me_delete(psy_auth_user):
    User = get_user_model()
    user_count = User.objects.count()
    url = '/api/v1/users/psychologists/me/'
    response = psy_auth_user.delete(url)
    assert user_count - 1 == User.objects.count()
    assert response.status_code == status.HTTP_204_NO_CONTENT


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
def test_psy_page_status(request,
                         test_client,
                         test_user,
                         expected,
                         notification):
    test_user = request.getfixturevalue(test_user)
    url = f'/api/v1/users/psychologists/{test_user.id}/'
    test_client = request.getfixturevalue(test_client)
    response = test_client.get(url)
    assert response.status_code == expected, notification.format(url)


# нужно запретить
@pytest.mark.xfail
def test_auth_user_reg(psy_auth_user):
    url = '/api/v1/users/psychologists/'
    response = psy_auth_user.post(url, {"email": "lkjasfnd424@mail.ru",
                                        "first_name": "ФродБэггинс",
                                        "last_name": "вафыавыф",
                                        "password": "Ss12345!",
                                        "birth_date": "2000-05-01"})
    assert response.status_code == status.HTTP_403_FORBIDDEN


# нужно запретить
@pytest.mark.xfail
def test_auth_user_reg_client(psy_auth_user):
    url = '/api/v1/users/psychologists/'
    response = psy_auth_user.post(url, {"email": "u1ser@example.com",
                                        "complaint": "Обязательное поле."})
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_anon_user_reg(psy_not_auth_user):
    url = '/api/v1/users/psychologists/'
    User = get_user_model()
    user_count = User.objects.count()
    response = psy_not_auth_user.post(url, {"email": "lkjasfnd424@mail.ru",
                                            "first_name": "ФродБэггинс",
                                            "last_name": "вафыавыф",
                                            "password": "Ss12345!",
                                            "birth_date": "2000-05-01"})
    assert user_count + 1 == User.objects.count()
    assert response.status_code == status.HTTP_201_CREATED


def test_anon_client_reg(psy_not_auth_user):
    url = '/api/v1/users/clients/'
    client_count = CustomClientUser.objects.count()
    response = psy_not_auth_user.post(url, {"email": "u1ser@example.com",
                                            "complaint": "Обязательное поле."})
    assert client_count + 1 == CustomClientUser.objects.count()
    assert response.status_code == status.HTTP_201_CREATED


def test_anon_user_put(psy_auth_user):
    url = '/api/v1/users/psychologists/me/'
    User = get_user_model()
    user_count = User.objects.count()
    response = psy_auth_user.put(url, {"email": "lkjasfnd424@mail.ru",
                                       "first_name": "ФродБэггинс",
                                       "last_name": "вафыавыф",
                                       "birth_date": "2000-05-01"})
    assert user_count == User.objects.count()
    assert response.status_code == status.HTTP_200_OK


def test_anon_user_patch(psy_auth_user):
    url = '/api/v1/users/psychologists/me/'
    User = get_user_model()
    user_count = User.objects.count()
    response = psy_auth_user.patch(url, {"first_name": "Фыва",
                                         "last_name": "Фымаа", })
    assert user_count == User.objects.count()
    assert response.status_code == status.HTTP_200_OK


def test_anon_user_delete(psy_auth_user):
    url = '/api/v1/users/psychologists/me/'
    User = get_user_model()
    user_count = User.objects.count()
    response = psy_auth_user.delete(url)
    assert user_count - 1 == User.objects.count()
    assert response.status_code == status.HTTP_204_NO_CONTENT
