from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/core/', include('core.urls')),
    path('api/beresht/', include('miyanBeresht.urls')),
    path('api/madi/', include('miyanMadi.urls')),
    path('api/group/', include('miyanGroup.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
