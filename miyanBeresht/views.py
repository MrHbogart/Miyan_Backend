# miyanBeresht/views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BereshtMenu, BereshtMenuSection, BereshtMenuItem
from .serializers import (
    BereshtMenuSerializer, 
    BereshtMenuSectionSerializer, 
    BereshtMenuItemSerializer
)

class BereshtMenuViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Beresht menus
    - GET: Available to all users
    - POST/PUT/DELETE: Admin only
    """
    queryset = BereshtMenu.objects.filter(is_active=True).prefetch_related(
        'sections__items'
    )
    serializer_class = BereshtMenuSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'])
    def main(self, request):
        """Get the main active menu (public endpoint)"""
        main_menu = self.queryset.filter(menu_type='main').first()
        if not main_menu:
            # If no main menu found, return the first active menu
            main_menu = self.queryset.first()
        
        if not main_menu:
            return Response({'detail': 'No active menu found'}, status=404)
            
        serializer = self.get_serializer(main_menu)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's special menu (public endpoint)"""
        today_menu = self.queryset.filter(menu_type='today').first()
        if not today_menu:
            return Response({'detail': 'No today\'s special menu found'}, status=404)
            
        serializer = self.get_serializer(today_menu)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def all(self, request):
        """Get all active menus (public endpoint)"""
        menus = self.queryset
        serializer = self.get_serializer(menus, many=True)
        return Response(serializer.data)


class BereshtMenuSectionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Beresht menu sections (Admin only for write operations)
    """
    queryset = BereshtMenuSection.objects.filter(is_active=True).prefetch_related('items')
    serializer_class = BereshtMenuSectionSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class BereshtMenuItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Beresht menu items (Admin only for write operations)
    """
    queryset = BereshtMenuItem.objects.filter(is_available=True)
    serializer_class = BereshtMenuItemSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
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