from django.urls import path, include, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/core/', include('core.urls')),
    path('api/beresht/', include('miyanBeresht.urls')),
    path('api/madi/', include('miyanMadi.urls')),
    path('api/group/', include('miyanGroup.urls')),

