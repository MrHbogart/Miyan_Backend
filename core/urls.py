from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]
