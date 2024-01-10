import re
from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_username(value):
    """Валидация username для моделей."""
    regex = re.compile('^(?=.*[A-Za-z0-9])[A-Za-z0-9_-]+$')
    if not regex.match(value):
        raise ValidationError('Разрешены латинские буквы,'
                              'цифры, знаки - и _.'
                              'Должны быть как минимум одна буква или цифра.')


def year_validator(value):
    """Валидация года окончания УЗ для моделей."""
    if value > timezone.now().year + 5:
        raise ValidationError('Год не может быть больше текущего на 5 лет!')
    if value < 1900:
        raise ValidationError('Год не может быть ранее 1900!')
