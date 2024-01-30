import re
from pathlib import Path

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


BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR_NAME = 'backend'
NGINX_DIR_NAME = 'infra'
DEPLOY_INFO_FILE_NAME = 'tests.yml'
DOCKERFILE_NAME = 'Dockerfile'
DOCKERHUB_USERNAME_KEY = 'dockerhub_username'
DOCKER_COMPOSE_PROD_FILE_NAME = 'docker-compose.production.yml'
DATETIMEFORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

for dir_name in (BACKEND_DIR_NAME, NGINX_DIR_NAME):
    path_to_dir = BASE_DIR / dir_name
    if not path_to_dir.is_dir():
        raise AssertionError(
            f'В директории `{BASE_DIR}` не найдена папка проекта '
            f'`{dir_name}/`. Убедитесь, что у вас верная структура проекта.'
        )


@pytest.fixture(scope='session')
def backend_dir_info() -> tuple[Path, str]:
    return (BASE_DIR / BACKEND_DIR_NAME, BACKEND_DIR_NAME)


@pytest.fixture(scope='session')
def dockerfile_name() -> str:
    return DOCKERFILE_NAME


@pytest.fixture(scope='session')
def nginx_dir_info() -> tuple[Path, str]:
    return (BASE_DIR / NGINX_DIR_NAME, NGINX_DIR_NAME)


@pytest.fixture(scope='session')
def expected_nginx_files() -> set[str]:
    return {'nginx.conf', 'Dockerfile'}


@pytest.fixture(scope='session')
def dockerhub_username_key() -> str:
    return DOCKERHUB_USERNAME_KEY


@pytest.fixture
def base_dir() -> Path:
    return BASE_DIR


@pytest.fixture
def workflow_file_name() -> str:
    return WORKFLOW_FILE


@pytest.fixture
def docker_compose_prod_file_name() -> str:
    return DOCKER_COMPOSE_PROD_FILE_NAME


@pytest.fixture(scope='session')
def deploy_file_info() -> tuple[Path, str]:
    deploy_info_file = BASE_DIR / DEPLOY_INFO_FILE_NAME
    assert deploy_info_file.is_file(), (
        f'Убедитесь, что в корневой директории проекта создан файл '
        f'`{DEPLOY_INFO_FILE_NAME}`'
    )
    return (deploy_info_file, DEPLOY_INFO_FILE_NAME)


@pytest.fixture(scope='session')
def deploy_info_file_content(
        deploy_file_info: tuple[Path, str]
) -> dict[str, str]:
    path, relative_path = deploy_file_info
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        file_content = {}
        line_pattern = re.compile(r'[\w_]+: ?[^;]+')
        for line_num, line in enumerate(f.readlines(), 1):
            if not line.strip():
                continue
            assert line_pattern.match(line), (
                f'Убедитесь, что строка номер {line_num} файла '
                f'`{relative_path}` соответствует шаблону: '
                '`<ключ>: <значение>`. В названии ключа '
                'допустимы буквы и нижнее подчеркивание.'
            )
            line = line.strip().strip(';')
            key, value = line.split(':', maxsplit=1)
            file_content[key.strip()] = value.strip()
    return file_content


@pytest.fixture(scope='session')
def expected_deploy_info_file_content() -> dict[str, str]:
    pass


@pytest.fixture(params=())
def link_key(request) -> str:
    return request.param


@pytest.fixture(scope='session')
def link_keys() -> tuple[str, str]:
    pass


@pytest.fixture(scope='session')
def kittygram_link_key() -> str:
    pass


@pytest.fixture(scope='session')
def taski_link_key() -> str:
    pass


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
