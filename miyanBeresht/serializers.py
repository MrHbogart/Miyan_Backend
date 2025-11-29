from rest_framework import serializers

from core.serializers import MenuPresentationSerializer
from .models import BereshtMenu, BereshtMenuItem


class BereshtMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BereshtMenuItem
        fields = [
            'id', 'name_fa', 'name_en', 'description_fa', 'description_en',
            'price_fa', 'price_en', 'display_order'
        ]


class BereshtMenuSerializer(MenuPresentationSerializer):
    sections = BereshtMenuSectionSerializer(many=True, read_only=True)
    
    class Meta:
        model = BereshtMenu
        fields = [
            'id', 'title_fa', 'title_en', 'subtitle_fa', 'subtitle_en',
            'is_active', 'display_order', 'sections', 'created_at', 'updated_at'
        ]
