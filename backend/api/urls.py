from django.urls import include, path
from rest_framework.routers import DefaultRouter
from djoser.views import UserViewSet

from .views import (UserMe, CustomClientUserViewSet, EducationViewSet)

router_users = DefaultRouter()

router_users.register('psychologists',
                      UserViewSet,
                      basename='psychologists',)

router_users.register('clients',
                      CustomClientUserViewSet,
                      basename='clients',)

router_users.register(r'psychologists/me/education',
                      EducationViewSet,
                      basename='education',)

urlpatterns = [
    path('users/psychologists/me/', UserMe.as_view()),
    path('users/', include(router_users.urls),),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/psychologists/', UserViewSet.as_view({'get': 'list',
                                                      'post': 'create'}),),

    # path('', include('djoser.urls')),
]