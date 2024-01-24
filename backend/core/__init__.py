import os

import yagmail


yag = yagmail.SMTP(
    os.getenv('GMAIL_USERNAME'),
    oauth2_file="./credentials.json"
)
