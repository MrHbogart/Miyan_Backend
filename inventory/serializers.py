from __future__ import annotations

from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from miyanGroup.models import Branch
from miyanGroup.serializers import BranchSerializer
from . import models


class BasicItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BasicItem
        fields = ['id', 'name', 'unit', 'unit_price', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecipeIngredient
        fields = ['id', 'basic_item', 'amount', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, required=False)

    class Meta:
        model = models.Recipe
        fields = ['id', 'name', 'price', 'ingredients', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def _sync_ingredients(self, recipe: models.Recipe, ingredients_data):
        """Create/update ingredient rows and remove ones omitted in the payload."""
        keep_ids = []
        for ingredient in ingredients_data:
            basic_item = ingredient['basic_item']
            amount = ingredient['amount']
            obj, _ = models.RecipeIngredient.objects.update_or_create(
                recipe=recipe,
                basic_item=basic_item,
                defaults={'amount': amount},
            )
            keep_ids.append(obj.id)

        prune_qs = models.RecipeIngredient.objects.filter(recipe=recipe)
        if keep_ids:
            prune_qs = prune_qs.exclude(id__in=keep_ids)
        prune_qs.delete()

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        with transaction.atomic():
            recipe = super().create(validated_data)
            if ingredients_data:
                self._sync_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
        with transaction.atomic():
            recipe = super().update(instance, validated_data)
            if ingredients_data is not None:
                self._sync_ingredients(recipe, ingredients_data)
        return recipe


class BranchBasicItemStockSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(
        source='branch',
        queryset=Branch.objects.filter(is_active=True),
        write_only=True,
    )
    item = serializers.PrimaryKeyRelatedField(queryset=models.BasicItem.objects.all())

    class Meta:
        model = models.BranchBasicItemStock
        fields = [
            'id',
            'branch',
            'branch_id',
            'item',
            'quantity',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class BranchRecipeStockSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(
        source='branch',
        queryset=Branch.objects.filter(is_active=True),
        write_only=True,
    )
    recipe = serializers.PrimaryKeyRelatedField(queryset=models.Recipe.objects.all())

    class Meta:
        model = models.BranchRecipeStock
        fields = [
            'id',
            'branch',
            'branch_id',
            'recipe',
            'quantity',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class InventoryAdjustmentSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(
        source='branch',
        queryset=Branch.objects.filter(is_active=True),
        write_only=True,
        required=False,
    )
    stock_before = serializers.DecimalField(max_digits=12, decimal_places=3, read_only=True)
    stock_after = serializers.DecimalField(max_digits=12, decimal_places=3, read_only=True)

    class Meta:
        model = models.InventoryAdjustment
        fields = [
            'id',
            'branch',
            'branch_id',
            'item_type',
            'basic_item',
            'recipe',
            'mode',
            'quantity',
            'stock_before',
            'stock_after',
            'note',
            'recorded_by',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['recorded_by', 'stock_before', 'stock_after', 'created_at', 'updated_at']

    def validate(self, attrs):
        item_type = attrs.get('item_type')
        basic_item = attrs.get('basic_item')
        recipe = attrs.get('recipe')
        mode = attrs.get('mode')
        quantity = attrs.get('quantity')

        if item_type == models.InventoryAdjustment.ItemType.BASIC:
            if not basic_item:
                raise serializers.ValidationError({'basic_item': 'Select a basic item.'})
            attrs['recipe'] = None
        elif item_type == models.InventoryAdjustment.ItemType.RECIPE:
            if not recipe:
                raise serializers.ValidationError({'recipe': 'Select a recipe.'})
            attrs['basic_item'] = None
        else:
            raise serializers.ValidationError({'item_type': 'Unknown item type.'})

        if quantity is None:
            raise serializers.ValidationError({'quantity': 'Quantity is required.'})
        if mode == models.InventoryAdjustment.Mode.SET and Decimal(quantity) < 0:
            raise serializers.ValidationError({'quantity': 'Quantity cannot be negative for set mode.'})
        return attrs

    def create(self, validated_data):
        branch = validated_data.get('branch')
        if not branch:
            raise serializers.ValidationError({'branch': 'Branch is required.'})

        item_type = validated_data['item_type']
        mode = validated_data['mode']
        quantity = validated_data['quantity']
        basic_item = validated_data.get('basic_item')
        recipe = validated_data.get('recipe')

        with transaction.atomic():
            if item_type == models.InventoryAdjustment.ItemType.BASIC:
                stock_obj, _ = models.BranchBasicItemStock.objects.select_for_update().get_or_create(
                    branch=branch,
                    item=basic_item,
                    defaults={'quantity': Decimal('0')},
                )
            else:
                stock_obj, _ = models.BranchRecipeStock.objects.select_for_update().get_or_create(
                    branch=branch,
                    recipe=recipe,
                    defaults={'quantity': Decimal('0')},
                )

            stock_before = stock_obj.quantity
            if mode == models.InventoryAdjustment.Mode.SET:
                new_quantity = quantity
            else:
                new_quantity = stock_before + quantity

            if new_quantity < 0:
                raise serializers.ValidationError({'quantity': 'Resulting stock cannot be negative.'})

            stock_obj.quantity = new_quantity
            stock_obj.save(update_fields=['quantity', 'updated_at'])

            validated_data['stock_before'] = stock_before
            validated_data['stock_after'] = new_quantity
            return super().create(validated_data)
