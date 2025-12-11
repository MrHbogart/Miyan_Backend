from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MadiMenuViewSet, MadiMenuItemViewSet,
    MadiInventoryItemViewSet, MadiInventoryRecordViewSet
)

router = DefaultRouter()
router.register(r'menu', MadiMenuViewSet, basename='madi-menu')
router.register(r'items', MadiMenuItemViewSet, basename='madi-items')
router.register(r'inventory/items', MadiInventoryItemViewSet, basename='madi-inventory-items')
router.register(r'inventory/records', MadiInventoryRecordViewSet, basename='madi-inventory-records')

urlpatterns = [
    path('', include(router.urls)),
]
