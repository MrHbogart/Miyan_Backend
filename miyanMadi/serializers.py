from rest_framework import serializers

from core.serializers import MenuPresentationSerializer
from .models import MadiMenu, MadiMenuSection, MadiMenuItem


class MadiMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MadiMenuItem
        fields = [
            'id', 'name_fa', 'name_en', 'description_fa', 'description_en',
            'price', 'price_fa', 'price_en', 'image', 'image_url',
            'is_available', 'is_todays_special', 'is_featured', 'is_chefs_special',
            'item_type', 'cuisine_type', 'ingredients_fa', 'ingredients_en',
            'cooking_method', 'serving_temperature', 'spice_level', 'portion_size',
            'is_vegetarian', 'is_vegan', 'is_gluten_free', 'contains_allergens',
            'preparation_time', 'calories', 'popularity_score', 'display_order'
        ]

class MadiMenuSectionSerializer(serializers.ModelSerializer):
    items = MadiMenuItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = MadiMenuSection
        fields = [
            'id', 'title_fa', 'title_en', 'description_fa', 'description_en',
            'section_type', 'meal_type', 'display_order', 'is_active', 'items'
        ]


class MadiMenuSerializer(MenuPresentationSerializer):
    sections = MadiMenuSectionSerializer(many=True, read_only=True)
    
    class Meta:
        model = MadiMenu
        fields = [
            'id', 'title_fa', 'title_en', 'subtitle_fa', 'subtitle_en',
            'menu_type', 'cover_image', 'service_hours', 'is_active', 'display_order',
            'valid_from', 'valid_until', 'sections', 'created_at', 'updated_at'
        ]
