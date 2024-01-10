from django.urls import include, path
from rest_framework.routers import DefaultRouter
from djoser.views import UserViewSet

from .views import (UserMe)

router_users = DefaultRouter()

# router_users.register('psychologists/',
#                 UserViewSet,
#                 basename='psychologists',)

urlpatterns = [
    path('users/psychologists/me/', UserMe.as_view()),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/psychologists/', UserViewSet.as_view({'get': 'list',
                                                      'post': 'create'}),),

    # path('', include('djoser.urls')),
]
