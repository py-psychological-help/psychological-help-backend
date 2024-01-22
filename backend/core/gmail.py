import os
from typing import Dict, List

from django.template import loader
import yagmail


def send_gmail(
    template: str, context: Dict, from_email: str, recipient_list: List
) -> None:
    """
    Регистрация в Gmail и отправка сообщения
    подробнее о библиотеке https://github.com/kootenpv/yagmail
    """
    msg = render_msg(template, context)
    yag = yagmail.SMTP(
        os.getenv('GMAIL_USERNAME'),
        oauth2_file="./credentials.json"
    )
    yag.send(recipient_list[0], 'Давай поговорим', msg)


def render_msg(template: str, context: Dict) -> str:
    """из полученного словаря рендерим html шаблон"""
    template = loader.get_template(template)
    return template.render(context)
