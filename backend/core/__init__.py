import os

import yagmail

from django.conf import settings

if settings.GMAIL_SEND_MESSAGE:
    yag = yagmail.SMTP(
        os.getenv('GMAIL_USERNAME'),
        oauth2_file="./credentials.json"
    )
