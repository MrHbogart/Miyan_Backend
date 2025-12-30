from rest_framework import serializers

from core.serializers import MenuPresentationSerializer
from .models import MadiMenu, MadiMenuSection, MadiMenuItem


class MadiMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MadiMenuItem
        fields = [
            'id', 'name_fa', 'name_en', 'description_fa', 'description_en',
            'price_fa', 'price_en', 'image', 'video', 'display_order'
        ]


class MadiMenuSectionSerializer(serializers.ModelSerializer):
    items = MadiMenuItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = MadiMenuSection
        fields = [
            'id', 'title_fa', 'title_en', 'description_fa', 'description_en',
            'display_order', 'is_active', 'is_main_section', 'items'
        ]


class MadiMenuSerializer(MenuPresentationSerializer):
    sections = MadiMenuSectionSerializer(many=True, read_only=True)
    
    class Meta:
        model = MadiMenu
        fields = [
            'id', 'title_fa', 'title_en', 'subtitle_fa', 'subtitle_en',
            'service_hours', 'is_active', 'show_images', 'menu_type', 'display_order', 'sections', 'created_at', 'updated_at'
        ]
