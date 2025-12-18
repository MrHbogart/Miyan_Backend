from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from . import models

User = get_user_model()


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Branch
        fields = ['id', 'name', 'code', 'address', 'is_active']


class StaffSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = models.Staff
        fields = [
            'id',
            'username',
            'email',
            'telegram_token',
            'telegram_id',
            'language_preference',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['telegram_token', 'created_at', 'updated_at']


class StaffRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(allow_blank=True, required=False)
    first_name = serializers.CharField(allow_blank=True, required=False)
    last_name = serializers.CharField(allow_blank=True, required=False)
    language_preference = serializers.ChoiceField(choices=[('fa', 'Persian'), ('en', 'Finglish')], default='fa')
    branch_id = serializers.IntegerField(required=False)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists.')
        return value

    def validate_branch_id(self, value):
        if value is None:
            return value
        if not models.Branch.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError('Branch not found or inactive.')
        return value

    def create(self, validated_data):
        branch_id = validated_data.pop('branch_id', None)
        password = validated_data.pop('password')
        language = validated_data.pop('language_preference', 'fa')
        user_fields = {k: validated_data.get(k, '') for k in ['username', 'email', 'first_name', 'last_name']}
        with transaction.atomic():
            user = User.objects.create_user(password=password, **user_fields)
            staff = models.Staff.objects.create(user=user, language_preference=language)
            if branch_id:
                branch = models.Branch.objects.get(id=branch_id)
                models.StaffBranchAssignment.objects.create(
                    staff=staff, branch=branch, is_primary=True
                )
        return staff


class StaffBranchAssignmentSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(
        source='branch',
        queryset=models.Branch.objects.filter(is_active=True),
        write_only=True,
    )

    class Meta:
        model = models.StaffBranchAssignment
        fields = ['id', 'branch', 'branch_id', 'is_primary', 'is_active', 'created_at', 'updated_at']


class StaffShiftSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)

    class Meta:
        model = models.StaffShift
        fields = ['id', 'branch', 'started_at', 'ended_at', 'created_at', 'updated_at']
        read_only_fields = ['started_at', 'ended_at', 'created_at', 'updated_at']


class StartShiftSerializer(serializers.Serializer):
    branch_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Branch.objects.filter(is_active=True), source='branch'
    )

    def create(self, validated_data):
        staff = self.context['staff']
        branch = validated_data['branch']
        if not models.StaffBranchAssignment.objects.filter(
            staff=staff,
            branch=branch,
            is_active=True,
        ).exists():
            raise serializers.ValidationError('Staff is not assigned to this branch.')
        # end any previous shift
        models.StaffShift.objects.filter(staff=staff, ended_at__isnull=True).update(ended_at=timezone.now())
        return models.StaffShift.objects.create(staff=staff, branch=branch)


class EndShiftSerializer(serializers.Serializer):
    def save(self, **kwargs):
        staff = self.context['staff']
        active = staff.active_shift
        if not active:
            raise serializers.ValidationError('No active shift to end.')
        active.ended_at = timezone.now()
        active.save(update_fields=['ended_at'])
        return active


class InventoryItemSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(
        source='branch', queryset=models.Branch.objects.filter(is_active=True), write_only=True
    )

    class Meta:
        model = models.InventoryItem
        fields = ['id', 'branch', 'branch_id', 'name', 'unit', 'is_active', 'created_at', 'updated_at']


class InventoryMeasurementSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)
    item = serializers.PrimaryKeyRelatedField(queryset=models.InventoryItem.objects.filter(is_active=True))

    class Meta:
        model = models.InventoryMeasurement
        fields = ['id', 'branch', 'item', 'quantity', 'recorded_by', 'measured_at', 'created_at']
        read_only_fields = ['branch', 'recorded_by', 'measured_at', 'created_at']


class InventoryInputSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)
    item = serializers.PrimaryKeyRelatedField(queryset=models.InventoryItem.objects.filter(is_active=True))

    class Meta:
        model = models.InventoryInput
        fields = ['id', 'branch', 'item', 'quantity', 'note', 'recorded_by', 'recorded_at', 'created_at']
        read_only_fields = ['branch', 'recorded_by', 'recorded_at', 'created_at']

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError('Quantity must be non-negative.')
        if value > 1_000_000:
            raise serializers.ValidationError('Quantity is out of expected range.')
        return value


class InventoryTransactionSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)
    item = serializers.PrimaryKeyRelatedField(queryset=models.InventoryItem.objects.filter(is_active=True))

    class Meta:
        model = models.InventoryTransaction
        fields = ['id', 'branch', 'item', 'note', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['branch', 'created_by', 'created_at', 'updated_at']


class TelegramLinkSerializer(serializers.Serializer):
    telegram_token = serializers.CharField()
    telegram_id = serializers.CharField(required=False, allow_blank=True)


class TelegramTokenExchangeSerializer(serializers.Serializer):
    telegram_token = serializers.CharField()

    def create(self, validated_data):
        staff = validated_data['staff']
        token, _ = Token.objects.get_or_create(user=staff.user)
        return token


class MiyanGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MiyanGallery
        fields = '__all__'
