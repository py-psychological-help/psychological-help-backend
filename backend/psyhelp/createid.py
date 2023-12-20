import random
import string


from chat.models import Chat



def create_randomid():
    later = string.ascii_letters + '0123456789'
    while True:
        id = ''
        for i in range(4):
            id += random.choice(later)
        if not Chat.objects.filter(chat_secret_key=id).exists():
            return id
    
