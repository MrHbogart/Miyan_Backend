# miyanBeresht/views.py
from core.viewsets import BaseMenuItemViewSet, BaseMenuViewSet
from .models import BereshtMenu, BereshtMenuItem
from .serializers import BereshtMenuSerializer, BereshtMenuItemSerializer


class BereshtMenuViewSet(BaseMenuViewSet):
    """API endpoint for Beresht menus."""

    queryset = BereshtMenu.objects.all().prefetch_related('sections__items')
    serializer_class = BereshtMenuSerializer


class BereshtMenuItemViewSet(BaseMenuItemViewSet):
    """API endpoint for Beresht menu items."""

    queryset = BereshtMenuItem.objects.all()
    serializer_class = BereshtMenuItemSerializer
