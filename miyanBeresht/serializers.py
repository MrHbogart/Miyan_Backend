from rest_framework import serializers

from core.serializers import MenuPresentationSerializer
from .models import (
    BereshtMenu, BereshtMenuSection, BereshtMenuItem,
    BereshtInventoryItem, BereshtInventoryRecord
)


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


class BereshtInventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BereshtInventoryItem
        fields = ['id', 'name', 'unit']


class BereshtInventoryRecordSerializer(serializers.ModelSerializer):
    recorded_by = serializers.StringRelatedField(read_only=True)
    item = serializers.PrimaryKeyRelatedField(queryset=BereshtInventoryItem.objects.all())

    class Meta:
        model = BereshtInventoryRecord
        fields = ['id', 'item', 'quantity', 'note', 'recorded_by', 'recorded_at']
        read_only_fields = ['recorded_by', 'recorded_at']

    def create(self, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        validated_data['recorded_by'] = user if user and user.is_authenticated else None
        return super().create(validated_data)
