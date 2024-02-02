import pytest
from rest_framework.test import APIClient
from django.core.exceptions import FieldDoesNotExist

from users.models import CustomUser, CustomClientUser, Document
from users.tests.conftest import document


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


def test_document_create(document):
    pass