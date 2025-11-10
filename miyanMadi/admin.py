# miyanMadi/admin.py
from django.contrib import admin
from .models import MadiMenu, MadiMenuSection, MadiMenuItem

@admin.register(MadiMenuItem)
class MadiMenuItemAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'name_fa', 'section', 'item_type', 'price', 'is_available', 'is_todays_special', 'display_order']
    list_filter = ['is_available', 'is_todays_special', 'is_featured', 'is_chefs_special', 'item_type', 'cuisine_type', 'section']
    search_fields = ['name_en', 'name_fa', 'description_en', 'description_fa', 'ingredients_en', 'ingredients_fa']
    list_editable = ['price', 'is_available', 'is_todays_special', 'display_order']
    readonly_fields = ['popularity_score']

class MadiMenuItemInline(admin.TabularInline):
    model = MadiMenuItem
    extra = 1
    fields = ['name_en', 'name_fa', 'item_type', 'price', 'is_available', 'is_todays_special', 'display_order']

@admin.register(MadiMenuSection)
class MadiMenuSectionAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_fa', 'menu', 'section_type', 'meal_type', 'display_order', 'is_active']
    list_filter = ['section_type', 'meal_type', 'is_active', 'menu']
    search_fields = ['title_en', 'title_fa']
    inlines = [MadiMenuItemInline]

class MadiMenuSectionInline(admin.TabularInline):
    model = MadiMenuSection
    extra = 1
    fields = ['title_en', 'title_fa', 'section_type', 'meal_type', 'display_order', 'is_active']

@admin.register(MadiMenu)
class MadiMenuAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_fa', 'menu_type', 'is_active', 'created_at']
    list_filter = ['menu_type', 'is_active']
    search_fields = ['title_en', 'title_fa', 'subtitle_en', 'subtitle_fa']
    inlines = [MadiMenuSectionInline]