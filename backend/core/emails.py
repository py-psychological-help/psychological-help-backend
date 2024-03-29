from django.conf import settings
from .tasks import send_email_task


def send_confirmation_code(user, confirmation_code):
    """Оправка кода подтверждения почтты."""
    name = user.last_name + ' ' + user.first_name
    send_email_task.delay(
        'mail/email_confirmation.html',
        {'user': name, 'confirmation_code': confirmation_code},
        settings.EMAIL_HOST_USER,
        [user.email]
    )


def send_reg_confirm(user):
    """Оправка уведомления о успешной регистрации."""
    name = user.last_name + ' ' + user.first_name
    send_email_task.delay(
        'mail/registration_confirm.html',
        {'user': name},
        settings.EMAIL_HOST_USER,
        [user.email]
    )


def send_client_reg_confirm(user):
    """Оправка уведомления о успешной регистрации."""
    name = user.last_name + ' ' + user.first_name
    send_email_task.delay(
        'mail/client_registration_confirm.html',
        {'user': name},
        settings.EMAIL_HOST_USER,
        [user.email]
    )


def send_documents_confirm(user):
    """Оправка уведомления о проверки документов."""
    last_name = user.last_name
    first_name = user.first_name
    send_email_task.delay(
        'mail/documents_confirm.html',
        {
            'last_name': last_name,
            'first_name': first_name,
        },
        settings.EMAIL_HOST_USER,
        [user.email]
    )


def send_chat_url(chat):
    """Оправка клиенту ссылки на чат."""
    user = chat.client
    chat_secret_key = chat.chat_secret_key
    chat_url = (f'http://{settings.ALLOWED_HOSTS[-1]}/'
                f'client-side/{chat_secret_key}/')
    send_email_task.delay(
        'mail/chat_url.html',
        {'chat_url': chat_url},
        settings.EMAIL_HOST_USER,
        [user.email]
    )
