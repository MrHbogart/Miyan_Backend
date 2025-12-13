from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlameMonitorView

from .views import (
    BereshtMenuViewSet, BereshtMenuItemViewSet,
    BereshtInventoryItemViewSet, BereshtInventoryRecordViewSet
)

router = DefaultRouter()
router.register(r'menu', BereshtMenuViewSet, basename='beresht-menu')
router.register(r'items', BereshtMenuItemViewSet, basename='beresht-items')
router.register(r'inventory/items', BereshtInventoryItemViewSet, basename='beresht-inventory-items')
router.register(r'inventory/records', BereshtInventoryRecordViewSet, basename='beresht-inventory-records')

urlpatterns = [
    path('', include(router.urls)),
    path("flame/", FlameMonitorView.as_view(), name="flame-monitor"),
]
