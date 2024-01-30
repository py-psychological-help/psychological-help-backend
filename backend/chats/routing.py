from django.urls import path
from djangochannelsrestframework.consumers import view_as_consumer

from api.views import MessageViewSet
from . import consumers


websocket_urlpatterns = [
    path('ws/chat/<str:chat_secret_key>/', consumers.ChatConsumer.as_asgi()),
    # path('ws/chat/<str:chat_secret_key>/', view_as_consumer(MessageViewSet.as_view({'get': 'list'}))),

]

print(websocket_urlpatterns)