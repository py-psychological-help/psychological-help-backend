from celery import shared_task
from mail_templated import send_mail

from .gmail import send_gmail


@shared_task
def send_email_task(template_name, context, from_email, recipient_list):
    """Таска на отправку сообщений через SMTP"""
    send_mail(template_name, context, from_email, recipient_list)


@shared_task
def send_gmail_task(template_name, context, from_email, recipient_list):
    """Таска на отправку сообщений через gmail"""
    send_gmail(template_name, context, from_email, recipient_list)
