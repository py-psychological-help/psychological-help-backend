from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)
from djoser.views import UserViewSet

from .views import (UserMe, CustomClientUserViewSet,
                    DocumentViewSet, ChatViewSet, MessageViewSet,
                    activate_chat, finish_chat)

router = DefaultRouter()

router.register('users/psychologists',
                UserViewSet,
                basename='psychologists',)

router.register('users/clients',
                CustomClientUserViewSet,
                basename='clients',)

router.register(r'users/psychologists/me/documents',
                DocumentViewSet,
                basename='documents',)

router.register(r'chats/(?P<chat_secret_key>[a-zA-Z0-9]+)/messages',
                MessageViewSet,
                basename='message')
router.register('chats',
                ChatViewSet,
                basename='chats')
router.register('chats',
                ChatViewSet,
                basename='chats')

urlpatterns = [
    path('users/psychologists/me/', UserMe.as_view()),

    path('chats/<str:chat_secret_key>/start/',
         activate_chat,
         name='start_chat'),

    path('chats/<str:chat_secret_key>/finish/',
         finish_chat,
         name='finish_chat'),

    path('', include(router.urls),),

    path('api-token-auth/', views.obtain_auth_token),

    # path('api/token/',
         # TokenObtainPairView.as_view(),
         # name='token_obtain_pair'),

    # path('api/token/refresh/',
         # TokenRefreshView.as_view(),
         # name='token_refresh'),

    # path('api/token/verify/',
         # TokenVerifyView.as_view(),
         # name='token_verify'),

    path('auth/',
         include('djoser.urls')),

    path('auth/',
         include('djoser.urls.authtoken')),

    # path('auth/',
         # include('djoser.urls.jwt')),

    path('users/psychologists/', UserViewSet.as_view({'get': 'list',
                                                      'post': 'create'}),),
]
