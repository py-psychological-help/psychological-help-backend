from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ChatViewSet, MessageViewSet

router_v1 = DefaultRouter()
router_v1.register('chats', ChatViewSet)
router_v1.register(
    r'chats/(?P<chat_id>\d+)/messages',
    MessageViewSet,
    basename='message'
)

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router_v1.urls))
]
