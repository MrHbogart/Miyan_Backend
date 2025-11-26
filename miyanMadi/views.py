from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.viewsets import AdminWritePermissionMixin, MenuTypeActionMixin
from .models import MadiMenu, MadiMenuSection, MadiMenuItem
from .serializers import (
    MadiMenuSerializer, 
    MadiMenuSectionSerializer, 
    MadiMenuItemSerializer
)

class MadiMenuViewSet(
    AdminWritePermissionMixin, MenuTypeActionMixin, viewsets.ModelViewSet
):
    """
    API endpoint for Madi menus
    - GET: Available to all users
    - POST/PUT/DELETE: Admin only
    """
    queryset = MadiMenu.objects.filter(is_active=True).prefetch_related(
        'sections__items'
    )
    serializer_class = MadiMenuSerializer
    @action(detail=False, methods=['get'])
    def main(self, request):
        """Get the main active menu (public endpoint)"""
        return self.respond_with_menu_type(
            'main', fallback_first=True, not_found_message='No active menu found'
        )
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's special menu (public endpoint)"""
        return self.respond_with_menu_type(
            'today', not_found_message="No today's special menu found"
        )
    
    @action(detail=False, methods=['get'])
    def breakfast(self, request):
        """Get breakfast menu (public endpoint)"""
        return self.respond_with_menu_type(
            'breakfast', not_found_message='No breakfast menu found'
        )
    
    @action(detail=False, methods=['get'])
    def all(self, request):
        """Get all active menus (public endpoint)"""
        return self.list_active_menus()


class MadiMenuSectionViewSet(AdminWritePermissionMixin, viewsets.ModelViewSet):
    """
    API endpoint for Madi menu sections (Admin only for write operations)
    """
    queryset = MadiMenuSection.objects.filter(is_active=True).prefetch_related('items')
    serializer_class = MadiMenuSectionSerializer


class MadiMenuItemViewSet(AdminWritePermissionMixin, viewsets.ModelViewSet):
    """
    API endpoint for Madi menu items (Admin only for write operations)
    """
    queryset = MadiMenuItem.objects.filter(is_available=True)
    serializer_class = MadiMenuItemSerializer
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured menu items (public endpoint)"""
        featured_items = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(featured_items, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def todays_specials(self, request):
        """Get today's special items (public endpoint)"""
        special_items = self.queryset.filter(is_todays_special=True)
        serializer = self.get_serializer(special_items, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def chefs_specials(self, request):
        """Get chef's special items (public endpoint)"""
        chefs_specials = self.queryset.filter(is_chefs_special=True)
        serializer = self.get_serializer(chefs_specials, many=True)
        return Response(serializer.data)
