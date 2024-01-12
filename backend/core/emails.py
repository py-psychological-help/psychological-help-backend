from mail_templated import send_mail

from django.conf import settings


def send_confirmation_code(user, confirmation_code):
    """Оправка кода подтверждения почтты."""
    send_mail('mail/email_confirmation.html',
              {'user': user,
               'confirmation_code': confirmation_code},
              settings.EMAIL_HOST_USER,
              [user.email])


def send_reg_confirm(user):
    """Оправка уведомления о успешной регистрации."""
    send_mail('mail/registration_confirm.html',
              {'user': user},
              settings.EMAIL_HOST_USER,
              [user.email])


def send_education_confirm(user):
    """Оправка уведомления о проверки документов."""
    send_mail('mail/education_confirm.html',
              {'user': user},
              settings.EMAIL_HOST_USER,
              [user.email])


def send_chat_url(chat):
    """Оправка клиенту ссылки на чат."""
    user = chat.client
    chat_url = f'http://letstalk.ddns.net/chats/{chat.id}/'
    send_mail('mail/chat_url.html',
              {'user': user,
               'chat_url': chat_url
               },
              settings.EMAIL_HOST_USER,
              [user.email])
