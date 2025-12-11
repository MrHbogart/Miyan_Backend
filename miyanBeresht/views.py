# miyanBeresht/views.py
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.viewsets import BaseMenuItemViewSet, BaseMenuViewSet
from .models import (
    BereshtMenu, BereshtMenuItem,
    BereshtInventoryItem, BereshtInventoryRecord
)
from .serializers import (
    BereshtMenuSerializer, BereshtMenuItemSerializer,
    BereshtInventoryItemSerializer, BereshtInventoryRecordSerializer
)


class BereshtMenuViewSet(BaseMenuViewSet):
    """API endpoint for Beresht menus."""

    queryset = BereshtMenu.objects.all().prefetch_related('sections__items')
    serializer_class = BereshtMenuSerializer


class BereshtMenuItemViewSet(BaseMenuItemViewSet):
    """API endpoint for Beresht menu items."""

    queryset = BereshtMenuItem.objects.all()
    serializer_class = BereshtMenuItemSerializer


class BereshtInventoryItemViewSet(ReadOnlyModelViewSet):
    """API endpoint for Beresht inventory items."""
    queryset = BereshtInventoryItem.objects.all()
    serializer_class = BereshtInventoryItemSerializer
    permission_classes = [AllowAny]


class BereshtInventoryRecordViewSet(viewsets.ModelViewSet):
    """API endpoint for Beresht inventory records."""
    queryset = BereshtInventoryRecord.objects.all()
    serializer_class = BereshtInventoryRecordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)
