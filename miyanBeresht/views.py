# miyanBeresht/views.py
from core.viewsets import (
    BaseMenuItemViewSet,
    BaseMenuSectionViewSet,
    BaseMenuViewSet,
)
from .models import BereshtMenu, BereshtMenuSection, BereshtMenuItem
from .serializers import (
    BereshtMenuSerializer, 
    BereshtMenuSectionSerializer, 
    BereshtMenuItemSerializer
)

class BereshtMenuViewSet(BaseMenuViewSet):
    """API endpoint for Beresht menus."""

    queryset = BereshtMenu.objects.all().prefetch_related('sections__items')
    serializer_class = BereshtMenuSerializer


class BereshtMenuSectionViewSet(BaseMenuSectionViewSet):
    """API endpoint for Beresht menu sections."""

    queryset = BereshtMenuSection.objects.all().prefetch_related('items')
    serializer_class = BereshtMenuSectionSerializer


class BereshtMenuItemViewSet(BaseMenuItemViewSet):
    """API endpoint for Beresht menu items."""

    queryset = BereshtMenuItem.objects.all()
    serializer_class = BereshtMenuItemSerializer
