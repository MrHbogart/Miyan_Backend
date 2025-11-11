from django.contrib import admin
from .models import BereshtMenu, BereshtMenuSection, BereshtMenuItem

@admin.register(BereshtMenuItem)
class BereshtMenuItemAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'name_fa', 'section', 'price', 'is_available', 'is_todays_special', 'display_order']
    list_filter = ['is_available', 'is_todays_special', 'is_featured', 'item_type', 'section']
    search_fields = ['name_en', 'name_fa', 'description_en', 'description_fa']
    list_editable = ['price', 'is_available', 'is_todays_special', 'display_order']

class BereshtMenuItemInline(admin.TabularInline):
    model = BereshtMenuItem
    extra = 1
    fields = ['name_en', 'name_fa', 'price', 'is_available', 'display_order']

@admin.register(BereshtMenuSection)
class BereshtMenuSectionAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_fa', 'menu', 'section_type', 'display_order', 'is_active']
    list_filter = ['section_type', 'is_active', 'menu']
    inlines = [BereshtMenuItemInline]

class BereshtMenuSectionInline(admin.TabularInline):
    model = BereshtMenuSection
    extra = 1
    fields = ['title_en', 'title_fa', 'section_type', 'display_order', 'is_active']

@admin.register(BereshtMenu)
class BereshtMenuAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_fa', 'menu_type', 'is_active', 'created_at']
    list_filter = ['menu_type', 'is_active']
    inlines = [BereshtMenuSectionInline]