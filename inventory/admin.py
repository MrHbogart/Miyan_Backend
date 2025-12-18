from django.contrib import admin

from . import models


@admin.register(models.BasicItem)
class BasicItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit', 'unit_price', 'created_at', 'updated_at')
    search_fields = ('name', 'unit')


class RecipeIngredientInline(admin.TabularInline):
    model = models.RecipeIngredient
    extra = 0
    autocomplete_fields = ('basic_item',)


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'created_at', 'updated_at')
    search_fields = ('name',)
    inlines = [RecipeIngredientInline]


@admin.register(models.BranchBasicItemStock)
class BranchBasicItemStockAdmin(admin.ModelAdmin):
    list_display = ('id', 'branch', 'item', 'quantity', 'updated_at')
    list_filter = ('branch',)
    search_fields = ('item__name',)
    autocomplete_fields = ('branch', 'item')


@admin.register(models.BranchRecipeStock)
class BranchRecipeStockAdmin(admin.ModelAdmin):
    list_display = ('id', 'branch', 'recipe', 'quantity', 'updated_at')
    list_filter = ('branch',)
    search_fields = ('recipe__name',)
    autocomplete_fields = ('branch', 'recipe')


@admin.register(models.InventoryAdjustment)
class InventoryAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'branch', 'item_type', 'mode', 'quantity', 'stock_before', 'stock_after', 'created_at', 'recorded_by')
    list_filter = ('branch', 'item_type', 'mode')
    search_fields = ('basic_item__name', 'recipe__name', 'note')
    autocomplete_fields = ('branch', 'basic_item', 'recipe', 'recorded_by')

