from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from . import models


class MianBereshtMenu1Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.MianBereshtMenu1
        fields = '__all__'


class MianBereshtMenu2Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.MianBereshtMenu2
        fields = '__all__'


class MianMadiMenu1Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.MianMadiMenu1
        fields = '__all__'


class MianMadiMenu2Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.MianMadiMenu2
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(queryset=models.Ingredient.objects.all(), source='ingredient', write_only=True)

    class Meta:
        model = models.RecipeIngredient
        fields = ('id', 'ingredient', 'ingredient_id', 'quantity', 'unit')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(source='recipeingredient_set', many=True, read_only=True)

    class Meta:
        model = models.Recipe
        fields = ('id', 'name', 'instructions', 'prep_time_minutes', 'price_estimate', 'ingredients')


class StaffSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.Staff
        fields = ('id', 'user', 'role', 'phone', 'is_active')


class SellRecordSerializer(serializers.ModelSerializer):
    # accept either content object via content_type/app label & model or a direct item_name
    class Meta:
        model = models.SellRecord
        fields = ('id', 'content_type', 'object_id', 'item_name', 'price', 'quantity', 'total', 'sold_by', 'sold_at', 'notes')
        read_only_fields = ('total', 'sold_at')
