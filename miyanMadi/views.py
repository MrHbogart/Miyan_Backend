from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.viewsets import BaseMenuItemViewSet, BaseMenuViewSet
from .models import (
    MadiMenu, MadiMenuItem,
    MadiInventoryItem, MadiInventoryRecord
)
from .serializers import (
    MadiMenuSerializer, MadiMenuItemSerializer,
    MadiInventoryItemSerializer, MadiInventoryRecordSerializer
)


class MadiMenuViewSet(BaseMenuViewSet):
    """API endpoint for Madi menus."""

    queryset = MadiMenu.objects.all().prefetch_related('sections__items')
    serializer_class = MadiMenuSerializer
    breakfast_not_found_message = 'No breakfast menu found'

    @action(detail=False, methods=['get'])
    def breakfast(self, request):
        """Get breakfast menu (public endpoint)"""
        return self.respond_with_menu_type(
            'breakfast', not_found_message=self.breakfast_not_found_message
        )


class MadiMenuItemViewSet(BaseMenuItemViewSet):
    """API endpoint for Madi menu items."""

    queryset = MadiMenuItem.objects.all()
    serializer_class = MadiMenuItemSerializer


class MadiInventoryItemViewSet(ReadOnlyModelViewSet):
    """API endpoint for Madi inventory items."""
    queryset = MadiInventoryItem.objects.all()
    serializer_class = MadiInventoryItemSerializer
    permission_classes = [AllowAny]


class MadiInventoryRecordViewSet(viewsets.ModelViewSet):
    """API endpoint for Madi inventory records."""
    queryset = MadiInventoryRecord.objects.all()
    serializer_class = MadiInventoryRecordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)

