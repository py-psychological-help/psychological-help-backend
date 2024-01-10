from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (UserMe)

router = DefaultRouter()

urlpatterns = [
    path('users/me/', UserMe.as_view()),
    path('auth/', include('djoser.urls.authtoken')),

    path('', include(router.urls),),
    path('', include('djoser.urls')),
]
