import re

from django.core.exceptions import ValidationError


def validate_username(value):
    """Валидация username для моделей."""
    regex = re.compile('^(?=.*[A-Za-z0-9])[A-Za-z0-9_-]+$')
    if not regex.match(value):
        raise ValidationError('Разрешены латинские буквы,'
                              'цифры, знаки - и _.'
                              'Должны быть как минимум одна буква или цифра.')
