from rest_framework import serializers

from core.serializers import MenuPresentationSerializer
from .models import BereshtMenu, BereshtMenuSection, BereshtMenuItem


class BereshtMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BereshtMenuItem
        fields = [
            'id', 'name_fa', 'name_en', 'description_fa', 'description_en',
            'price', 'price_fa', 'price_en', 'image', 'image_url',
            'is_available', 'is_todays_special', 'is_featured',
            'item_type', 'ingredients_fa', 'ingredients_en',
            'available_sizes', 'spice_level', 'is_vegetarian', 'is_vegan',
            'is_gluten_free', 'contains_allergens', 'preparation_time', 'calories',
            'display_order'
        ]

class BereshtMenuSectionSerializer(serializers.ModelSerializer):
    items = BereshtMenuItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = BereshtMenuSection
        fields = [
            'id', 'title_fa', 'title_en', 'description_fa', 'description_en',
            'section_type', 'display_order', 'is_active', 'items'
        ]


class BereshtMenuSerializer(MenuPresentationSerializer):
    sections = BereshtMenuSectionSerializer(many=True, read_only=True)
    
    class Meta:
        model = BereshtMenu
        fields = [
            'id', 'title_fa', 'title_en', 'subtitle_fa', 'subtitle_en',
            'menu_type', 'cover_image', 'is_active', 'display_order',
            'valid_from', 'valid_until', 'sections', 'created_at', 'updated_at'
        ]
