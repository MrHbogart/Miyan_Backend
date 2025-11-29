from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BereshtMenuViewSet, BereshtMenuItemViewSet

router = DefaultRouter()
router.register(r'beresht_menu', BereshtMenuViewSet, basename='beresht-menu')
router.register(r'beresht_items', BereshtMenuItemViewSet, basename='beresht-items')

urlpatterns = [
    path('', include(router.urls)),
]