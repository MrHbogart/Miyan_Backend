from django.contrib import admin
from . import models


@admin.register(models.MianBereshtMenu1)
class MianBereshtMenu1Admin(admin.ModelAdmin):
	list_display = ('name', 'price', 'available', 'created_at')
	search_fields = ('name',)


@admin.register(models.MianBereshtMenu2)
class MianBereshtMenu2Admin(admin.ModelAdmin):
	list_display = ('name', 'price', 'available', 'created_at')
	search_fields = ('name',)


@admin.register(models.MianMadiMenu1)
class MianMadiMenu1Admin(admin.ModelAdmin):
	list_display = ('name', 'price', 'available', 'created_at')
	search_fields = ('name',)


@admin.register(models.MianMadiMenu2)
class MianMadiMenu2Admin(admin.ModelAdmin):
	list_display = ('name', 'price', 'available', 'created_at')
	search_fields = ('name',)


@admin.register(models.Staff)
class StaffAdmin(admin.ModelAdmin):
	list_display = ('user', 'role', 'phone', 'is_active')
	search_fields = ('user__username', 'user__email', 'role')


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
	list_display = ('name', 'unit', 'stock_quantity', 'cost_per_unit')
	search_fields = ('name',)


class RecipeIngredientInline(admin.TabularInline):
	model = models.RecipeIngredient
	extra = 1


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
	list_display = ('name', 'prep_time_minutes', 'price_estimate')
	inlines = (RecipeIngredientInline,)


@admin.register(models.SellRecord)
class SellRecordAdmin(admin.ModelAdmin):
	list_display = ('item_name', 'price', 'quantity', 'total', 'sold_at', 'sold_by')
	search_fields = ('item_name',)
