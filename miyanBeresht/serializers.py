from rest_framework import serializers
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

class BereshtMenuSerializer(serializers.ModelSerializer):
    sections = BereshtMenuSectionSerializer(many=True, read_only=True)
    
    class Meta:
        model = BereshtMenu
        fields = [
            'id', 'title_fa', 'title_en', 'subtitle_fa', 'subtitle_en',
            'menu_type', 'cover_image', 'is_active', 'display_order',
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
            # item here is a dict produced by the child serializer
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
                    'fa': item.get('price_fa') or (str(price_val) if price_val is not None else ''),
                    'en': item.get('price_en') or (str(price_val) if price_val is not None else '')
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