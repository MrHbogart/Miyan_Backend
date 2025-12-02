from rest_framework import serializers

from core.serializers import MenuPresentationSerializer
from .models import BereshtMenu, BereshtMenuSection, BereshtMenuItem


class BereshtMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BereshtMenuItem
        fields = [
            'id', 'name_fa', 'name_en', 'description_fa', 'description_en',
            'price_fa', 'price_en', 'image', 'video', 'display_order'
        ]


class BereshtMenuSectionSerializer(serializers.ModelSerializer):
    items = BereshtMenuItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = BereshtMenuSection
        fields = [
            'id', 'title_fa', 'title_en', 'description_fa', 'description_en',
            'display_order', 'is_active', 'items'
        ]


class BereshtMenuSerializer(MenuPresentationSerializer):
    sections = BereshtMenuSectionSerializer(many=True, read_only=True)
    
    class Meta:
        model = BereshtMenu
        fields = [
            'id', 'title_fa', 'title_en', 'subtitle_fa', 'subtitle_en',
            'is_active', 'show_images', 'display_order', 'sections', 'created_at', 'updated_at'
        ]
