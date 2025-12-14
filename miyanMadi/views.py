from rest_framework import viewsets
from rest_framework.decorators import action

from core.viewsets import BaseMenuItemViewSet, BaseMenuViewSet
from .models import MadiMenu, MadiMenuItem
from .serializers import MadiMenuSerializer, MadiMenuItemSerializer


class MadiMenuViewSet(BaseMenuViewSet):
    """API endpoint for Madi menus."""

    queryset = MadiMenu.objects.select_related('branch').filter(branch__code='madi').prefetch_related('sections__items')
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

    queryset = MadiMenuItem.objects.filter(section__menu__branch__code='madi')
    serializer_class = MadiMenuItemSerializer
