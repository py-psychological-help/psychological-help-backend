from celery import shared_task
from mail_templated import send_mail

from django.conf import settings
from .gmail import send_gmail

# На ревью. Здесь используется Celery 
@shared_task
def send_email_task(template_name, context, from_email, recipient_list):
    """Таска на отправку сообщений через SMTP или gmail"""
    if settings.GMAIL_SEND_MESSAGE:
        send_gmail(template_name, context, from_email, recipient_list)
    else:
        send_mail(template_name, context, from_email, recipient_list)
