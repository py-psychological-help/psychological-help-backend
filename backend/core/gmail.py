from typing import Dict
import os.path
import base64

from email.mime.text import MIMEText
from django.template import loader
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def authorized_gmail() -> Credentials:
    """Авторизация в gmail api.
    для получения токена необходим credentials.json
    получить можно через google api при создании OAuth пользлвателя,
    https://developers.google.com/gmail/api/quickstart/python?hl=en

    положить файл рядом со скриптом

    при первом запуске откроется браузер, нужно зайти в акаунт гугл и дать разрешение
    после этого загрузится token.json в папку проекта.

    если уже есть токен, достаточно положить его в папку проекта
    """
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        for label in labels:
            print(label['name'])

    except HttpError as error:
        pass
        # print(f'An error occurred: {error}')
 
    return creds


def send_mail(template_name: str,
              context: Dict,
              recipient: str) -> None:
    """Авторизовываемся, рендерим текст, отправляем сообщение"""

    creds = authorized_gmail()
    message_text = render_msg(template_name, context)

    try:
        service = build("gmail", "v1", credentials=creds)
        message = MIMEText(message_text, 'html')

        message["To"] = recipient
        message["Subject"] = "Давай поговорим"


        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": encoded_message}

        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )

    except HttpError as error:
        send_message = None


def render_msg(template: str, context: Dict) -> str:
    """из полученного словаря рендерим html шаблон"""
    template = loader.get_template(template)
    return template.render(context)
