from decimal import Decimal, InvalidOperation

from rest_framework import serializers
from .models import MadiMenu, MadiMenuSection, MadiMenuItem


def format_decimal_string(value: Decimal) -> str:
    as_string = format(value, 'f')
    if '.' in as_string:
        as_string = as_string.rstrip('0').rstrip('.')
    return as_string


def format_price_display(value, fallback, lang: str) -> str:
    fallback = fallback or ''
    if value in (None, ''):
        return fallback
    try:
        decimal_value = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return fallback or str(value)

    thousands = decimal_value / Decimal('1000')

    if lang == 'fa':
        if thousands == thousands.to_integral_value():
            return str(int(thousands))
        return format_decimal_string(thousands)

    formatted = format_decimal_string(thousands)
    return f"IRR {formatted}"


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

class MadiMenuSerializer(serializers.ModelSerializer):
    sections = MadiMenuSectionSerializer(many=True, read_only=True)
    
    class Meta:
        model = MadiMenu
        fields = [
            'id', 'title_fa', 'title_en', 'subtitle_fa', 'subtitle_en',
            'menu_type', 'cover_image', 'service_hours', 'is_active', 'display_order',
            'valid_from', 'valid_until', 'sections', 'created_at', 'updated_at'
        ]
    
    def to_representation(self, instance):
        """Transform to match frontend structure exactly"""
        data = super().to_representation(instance)
        # Transform to match your frontend structure
        title_fa = data.get('title_fa')
        title_en = data.get('title_en')
        subtitle_fa = data.get('subtitle_fa')
        subtitle_en = data.get('subtitle_en')

        def build_item(item):
            image = item.get('image_url') or item.get('image') or '/images/medium/default-menu.jpg'
            price_val = item.get('price')
            return {
                'name': {
                    'fa': item.get('name_fa'),
                    'en': item.get('name_en')
                },
                'description': {
                    'fa': item.get('description_fa') or '',
                    'en': item.get('description_en') or ''
                },
                'price': {
                    'fa': format_price_display(price_val, item.get('price_fa'), 'fa'),
                    'en': format_price_display(price_val, item.get('price_en'), 'en')
                },
                'image': image
            }

        sections_out = []
        for section in data.get('sections', []):
            if not section.get('is_active'):
                continue
            items = [build_item(item) for item in section.get('items', []) if item.get('is_available')]
            sections_out.append({
                'title': {'fa': section.get('title_fa'), 'en': section.get('title_en')},
                'items': items
            })

        todays_items = []
        for section in data.get('sections', []):
            for item in section.get('items', []):
                if item.get('is_todays_special') and item.get('is_available'):
                    todays_items.append(build_item(item))

        transformed = {
            'title': {'fa': title_fa, 'en': title_en},
            'subtitle': ({'fa': subtitle_fa, 'en': subtitle_en} if (subtitle_fa or subtitle_en) else None),
            'sections': sections_out,
            'todays': {
                'title': {'fa': 'آیتم‌های تازه امروز', 'en': "Today's Fresh"},
                'sections': [
                    {
                        'title': {'fa': 'پیشنهاد امروز', 'en': "Today's Special"},
                        'items': todays_items
                    }
                ]
            }
        }

        return transformed
