from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import FlameMonitorView, BereshtMenuViewSet, BereshtMenuItemViewSet

router = DefaultRouter()
router.register(r'menu', BereshtMenuViewSet, basename='beresht-menu')
router.register(r'items', BereshtMenuItemViewSet, basename='beresht-items')

urlpatterns = [
    path('', include(router.urls)),
    path("flame/", FlameMonitorView.as_view(), name="flame-monitor"),
]
