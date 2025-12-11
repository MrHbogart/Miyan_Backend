from rest_framework import serializers

from core.serializers import MenuPresentationSerializer
from .models import (
    MadiMenu, MadiMenuSection, MadiMenuItem,
    MadiInventoryItem, MadiInventoryRecord
)


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
            'display_order', 'is_active', 'items'
        ]


class MadiMenuSerializer(MenuPresentationSerializer):
    sections = MadiMenuSectionSerializer(many=True, read_only=True)
    
    class Meta:
        model = MadiMenu
        fields = [
            'id', 'title_fa', 'title_en', 'subtitle_fa', 'subtitle_en',
            'service_hours', 'is_active', 'show_images', 'display_order', 'sections', 'created_at', 'updated_at'
        ]


class MadiInventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MadiInventoryItem
        fields = ['id', 'name', 'unit']


class MadiInventoryRecordSerializer(serializers.ModelSerializer):
    recorded_by = serializers.StringRelatedField(read_only=True)
    item = serializers.PrimaryKeyRelatedField(queryset=MadiInventoryItem.objects.all())

    class Meta:
        model = MadiInventoryRecord
        fields = ['id', 'item', 'quantity', 'note', 'recorded_by', 'recorded_at']
        read_only_fields = ['recorded_by', 'recorded_at']

    def create(self, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        validated_data['recorded_by'] = user if user and user.is_authenticated else None
        return super().create(validated_data)
