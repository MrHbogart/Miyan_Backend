from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/core/', include('core.urls')),
    path('api/beresht/', include('miyanBeresht.urls')),
    path('api/madi/', include('miyanMadi.urls')),
    path('api/group/', include('miyanGroup.urls')),
]