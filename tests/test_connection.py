import json
import re
from http import HTTPStatus
from pathlib import Path
from typing import Optional

import requests


def _get_validated_link(
        deploy_file_info: tuple[Path, str],
        deploy_info_file_content: dict[str, str],
        link_key: str
) -> str:
    _, path_to_deploy_info_file = deploy_file_info
    assert link_key in deploy_info_file_content, (
        f'Убедитесь, что файл `{path_to_deploy_info_file}` содержит ключ '
        f'`{link_key}`.'
    )
    link: str = deploy_info_file_content[link_key]
    assert link.startswith('https'), (
        f'Убедитесь, что cсылка ключ `{link_key}` в файле '
        f'`{path_to_deploy_info_file}` содержит ссылку, которая начинается с '
        'префикса `https`.'
    )
    link_pattern = re.compile(
        r'^https:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.'
        r'[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$'
    )
    assert link_pattern.match(link), (
        f'Убедитесь, что ключ `{link_key}` в файле '
        f'`{path_to_deploy_info_file}` содержит корректную ссылку.'
    )
    return link.rstrip('/')


def _make_safe_request(link: str, stream: bool = False) -> requests.Response:
    try:
        response = requests.get(link, stream=stream, timeout=15)
    except requests.exceptions.SSLError:
        raise AssertionError(
            f'Убедитесь, что настроили шифрование для `{link}`.'
        )
    except requests.exceptions.ConnectionError:
        raise AssertionError(
            f'Убедитесь, что URL `{link}` доступен.'
        )
    expected_status = HTTPStatus.OK
    assert response.status_code == expected_status, (
        f'Убедитесь, что GET-запрос к `{link}` возвращает ответ со статусом '
        f'{int(expected_status)}.'
    )
    return response


def _get_js_link(response: requests.Response) -> Optional[str]:
    js_link_pattern = re.compile(r'static/js/[^\"]+')
    search_result = re.search(js_link_pattern, response.text)
    return search_result.group(0) if search_result else None


def test_link_connection(
        deploy_file_info: tuple[Path, str],
        deploy_info_file_content: dict[str, str],
        link_key: str
) -> None:
    pass
