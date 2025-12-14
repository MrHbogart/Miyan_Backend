from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'miyan_gallery', views.MiyanGalleryViewSet, basename='gallery')
router.register(r'branches', views.BranchViewSet, basename='branch')
router.register(r'staff', views.StaffViewSet, basename='staff')
router.register(r'staff/assignments', views.StaffAssignmentViewSet, basename='staff-assignment')
router.register(r'shifts', views.StaffShiftViewSet, basename='shift')
router.register(r'inventory/items', views.InventoryItemViewSet, basename='inventory-item')
router.register(r'inventory/measurements', views.InventoryMeasurementViewSet, basename='inventory-measurement')
router.register(r'inventory/inputs', views.InventoryInputViewSet, basename='inventory-input')

urlpatterns = [
    path('', include(router.urls)),
    path('telegram/link/', views.TelegramLinkView.as_view(), name='telegram-link'),
    path('telegram/token/', views.TelegramTokenExchangeView.as_view(), name='telegram-token'),
]
