from rest_framework import serializers
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
        transformed = {
            'title': {
                'fa': data['title_fa'],
                'en': data['title_en']
            },
            'subtitle': data['subtitle_fa'] and data['subtitle_en'] and {
                'fa': data['subtitle_fa'],
                'en': data['subtitle_en']
            } or None,
            'sections': [
                {
                    'title': {
                        'fa': section['title_fa'],
                        'en': section['title_en']
                    },
                    'items': [
                        {
                            'name': {
                                'fa': item['name_fa'],
                                'en': item['name_en']
                            },
                            'description': {
                                'fa': item['description_fa'] or '',
                                'en': item['description_en'] or ''
                            },
                            'price': {
                                'fa': item['price_fa'] or str(item['price']),
                                'en': item['price_en'] or str(item['price'])
                            },
                            'image': item['image_url'] or (item['image'] and item['image'].url) or '/images/medium/default-menu.jpg'
                        }
                        for item in section['items']
                        if item['is_available']
                    ]
                }
                for section in data['sections']
                if section['is_active']
            ],
            'todays': {
                'title': {'fa': 'آیتم‌های تازه امروز', 'en': "Today's Fresh"},
                'sections': [
                    {
                        'title': {'fa': 'پیشنهاد امروز', 'en': "Today's Special"},
                        'items': [
                            {
                                'name': {
                                    'fa': item['name_fa'],
                                    'en': item['name_en']
                                },
                                'description': {
                                    'fa': item['description_fa'] or '',
                                    'en': item['description_en'] or ''
                                },
                                'price': {
                                    'fa': item['price_fa'] or str(item['price']),
                                    'en': item['price_en'] or str(item['price'])
                                },
                                'image': item['image_url'] or (item['image'] and item['image'].url) or '/images/medium/default-menu.jpg'
                            }
                            for section in data['sections']
                            for item in section['items']
                            if item['is_todays_special'] and item['is_available']
                        ]
                    }
                ]
            }
        }
        
        return transformed