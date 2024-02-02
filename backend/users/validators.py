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
    r"^[a-z0-9_.-]+[^-]@[a-z0-9.-]+\.[a-z]{2,}$",
    ('Разрешены только строчные буквы латинского алфавита, цифры, и символы '
     '“@”, “-”, “_” и “.”'))


EmailSymbolsValidator = RegexValidator(
    r"^([^-])(?!.*\.\-)(?!.*\-\.)(?!.*\_\.)(?!.*\.\_)(?!.*\.\.)",
    ('Запрещено использование тире в начале и конце, двойных точек, '
     'специальных символов, а так же комбинаций точки с тире '
     'и символом нижнего подчеркивания'))


NameSymbolsValidator = RegexValidator(r"^[^- ][а-яА-ЯёЁ\s-]+[^- ]$",
                                      ('Разрешены только буквы русского '
                                       'алфавита, дефис, и символ пробела. '
                                       'Дефисы и пробелы не могут находиться '
                                       'в начале и в конце ввода'))

NameSpacesValidator = RegexValidator(r"^(?!.*\s{2})(?!.*\-{2})",
                                     'Двойные дефисы и пробелы запрещены')


PasswordContentValidator = RegexValidator(
    r"[A-Za-z\d@$!%*#?&-]{8,20}$",
    ('Пароль должен содержать не менее восьми и не более двадцати символов, '
     'разрешены буквы латинского алфавита, специальные символы '
     'без ограничений, а так же цифры. Регистр букв имеет значение'))


PasswordGroupsValidator = RegexValidator(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&-])",
    ('Пароль должен содержать как миним одну '
     'строчную букву, как минимум одну заглавную, '
     'как минимум одну цифру, и как минимуи один специальный символ'))
