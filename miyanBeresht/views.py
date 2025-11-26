# miyanBeresht/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.viewsets import AdminWritePermissionMixin, MenuTypeActionMixin
from .models import BereshtMenu, BereshtMenuSection, BereshtMenuItem
from .serializers import (
    BereshtMenuSerializer, 
    BereshtMenuSectionSerializer, 
    BereshtMenuItemSerializer
)

class BereshtMenuViewSet(
    AdminWritePermissionMixin, MenuTypeActionMixin, viewsets.ModelViewSet
):
    """
    API endpoint for Beresht menus
    - GET: Available to all users
    - POST/PUT/DELETE: Admin only
    """
    queryset = BereshtMenu.objects.filter(is_active=True).prefetch_related(
        'sections__items'
    )
    serializer_class = BereshtMenuSerializer
    
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
    def all(self, request):
        """Get all active menus (public endpoint)"""
        return self.list_active_menus()


class BereshtMenuSectionViewSet(AdminWritePermissionMixin, viewsets.ModelViewSet):
    """
    API endpoint for Beresht menu sections (Admin only for write operations)
    """
    queryset = BereshtMenuSection.objects.filter(is_active=True).prefetch_related('items')
    serializer_class = BereshtMenuSectionSerializer


class BereshtMenuItemViewSet(AdminWritePermissionMixin, viewsets.ModelViewSet):
    """
    API endpoint for Beresht menu items (Admin only for write operations)
    """
    queryset = BereshtMenuItem.objects.filter(is_available=True)
    serializer_class = BereshtMenuItemSerializer
    
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
