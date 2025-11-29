from django.contrib import admin
from .models import BereshtMenu, BereshtMenuItem


@admin.register(BereshtMenuItem)
class BereshtMenuItemAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'name_fa', 'section', 'price_fa', 'display_order']
    list_filter = ['section']
    search_fields = ['name_en', 'name_fa', 'description_en', 'description_fa']
    list_editable = ['price_fa', 'display_order']


class BereshtMenuItemInline(admin.TabularInline):
    model = BereshtMenuItem
    extra = 1
    fields = ['name_en', 'name_fa', 'price_fa', 'display_order']


@admin.register(BereshtMenu)
class BereshtMenuAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_fa', 'is_active', 'created_at']
    list_filter = ['is_active']
    inlines = [BereshtMenuItemInline]