from django.urls import include, path
from rest_framework import routers

from .views import HealthcheckView

router = routers.DefaultRouter()

urlpatterns = [
    path('health/', HealthcheckView.as_view(), name='core-health'),
    path('', include(router.urls)),
]
