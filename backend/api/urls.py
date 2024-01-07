from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import ChatViewSet, MessageViewSet


router = DefaultRouter()

router.register('api/v1/chats', ChatViewSet, basename='chat')
router.register('api/v1/messages', MessageViewSet, basename='message')


urlpatterns = [
    path('', include(router.urls)),
]
