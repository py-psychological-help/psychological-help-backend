import re
from datetime import date

from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def year_validator(value):
    """Валидация года окончания УЗ для моделей."""
    if value > timezone.now().year + 5:
        raise ValidationError('Год не может быть больше текущего на 5 лет!')
    if value < 1900:
        raise ValidationError('Год не может быть ранее 1900!')


def birthday_validator(value):
    """Валидация дня рождения для моделей Пользователей."""
    age = (date.today() - value).days / 365
    if age < 18:
        raise ValidationError('Вам должно быть более 18 лет для регистрации!')
    if age > 200:
        raise ValidationError('Возраст не может быть более 200 лет!')


AlphanumericValidator = RegexValidator(
    r"^[a-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[a-z0-9.-]+$",
    '''Разрешены только строчные буквы латинского
    алфавита, цифры, и символы
    “@”, “-”, “_” и “.”. ''')

NameValidator = RegexValidator(r"^([А-ЯЁ][а-яё]+[\-\s]?){3,}",
                               '''Разрешены только буквы русского алфавита,
                               дефис, и символ пробела''')
