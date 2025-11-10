# miyanMadi/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MadiMenuViewSet, MadiMenuSectionViewSet, MadiMenuItemViewSet

router = DefaultRouter()
router.register(r'madi_menu', MadiMenuViewSet, basename='madi-menu')
router.register(r'madi_sections', MadiMenuSectionViewSet, basename='madi-sections')
router.register(r'madi_items', MadiMenuItemViewSet, basename='madi-items')

urlpatterns = [
    path('api/', include(router.urls)),
]