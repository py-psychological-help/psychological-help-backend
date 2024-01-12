from django.urls import include, path
from rest_framework.routers import DefaultRouter
from djoser.views import UserViewSet

from .views import (UserMe, CustomClientUserViewSet, EducationViewSet,
                    ChatViewSet, MessageViewSet, activate_chat, finish_chat)

router = DefaultRouter()

router.register('users/psychologists',
                      UserViewSet,
                      basename='psychologists',)

router.register('users/clients',
                      CustomClientUserViewSet,
                      basename='clients',)

router.register(r'user/psychologists/me/education',
                      EducationViewSet,
                      basename='education',)

router.register(r'chats/(?P<chat_id>\d+)/messages',
    MessageViewSet,
    basename='message'
)
router.register('chats',
                ChatViewSet,
                basename='chats'
)
router.register('chats',
                ChatViewSet,
                basename='chats'
)

urlpatterns = [
    path('users/psychologists/me/', UserMe.as_view()),
    path('chats/<int:chat_id>/start/', activate_chat, name='start_chat'),
    path('chats/<int:chat_id>/finish/', finish_chat, name='finish_chat'),
    path('', include(router.urls),),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/psychologists/', UserViewSet.as_view({'get': 'list',
                                                      'post': 'create'}),),

    # path('', include('djoser.urls')),
]
