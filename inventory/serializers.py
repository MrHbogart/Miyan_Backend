from rest_framework import serializers
from . import models


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Branch
        fields = ['id', 'name', 'location']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = ['id', 'name', 'unit']


class InventoryRecordSerializer(serializers.ModelSerializer):
    recorded_by = serializers.StringRelatedField(read_only=True)
    branch = serializers.PrimaryKeyRelatedField(queryset=models.Branch.objects.all())
    item = serializers.PrimaryKeyRelatedField(queryset=models.Item.objects.all())

    class Meta:
        model = models.InventoryRecord
        fields = ['id', 'branch', 'item', 'quantity', 'note', 'recorded_by', 'recorded_at']
        read_only_fields = ['recorded_by', 'recorded_at']

    def create(self, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        validated_data['recorded_by'] = user if user and user.is_authenticated else None
        return super().create(validated_data)


class StaffLinkSerializer(serializers.Serializer):
    bot_token = serializers.CharField()
    telegram_id = serializers.CharField()
