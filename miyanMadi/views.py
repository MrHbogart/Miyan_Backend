from rest_framework.decorators import action

from core.viewsets import BaseMenuItemViewSet, BaseMenuViewSet
from .models import MadiMenu, MadiMenuItem
from .serializers import MadiMenuSerializer, MadiMenuItemSerializer


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
    
    @action(detail=False, methods=['get'])
    def chefs_specials(self, request):
        """Get chef's special items (public endpoint)"""
        return self._special_response(is_chefs_special=True)
