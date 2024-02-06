from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from api.views import ActivateUser


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('api/v1/activate/<uid>/<token>/',
         ActivateUser.as_view({'get': 'activation'}),
         name='activation'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
