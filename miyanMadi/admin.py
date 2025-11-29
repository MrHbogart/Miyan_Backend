from django.contrib import admin
from .models import MadiMenu, MadiMenuSection, MadiMenuItem


@admin.register(MadiMenuItem)
class MadiMenuItemAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'name_fa', 'section', 'price_fa', 'display_order']
    list_filter = ['section']
    search_fields = ['name_en', 'name_fa', 'description_en', 'description_fa']
    list_editable = ['price_fa', 'display_order']


class MadiMenuItemInline(admin.TabularInline):
    model = MadiMenuItem
    extra = 1
    fields = ['name_en', 'name_fa', 'price_fa', 'display_order']


@admin.register(MadiMenuSection)
class MadiMenuSectionAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_fa', 'menu', 'display_order', 'is_active']
    list_filter = ['is_active', 'menu']
    inlines = [MadiMenuItemInline]


@admin.register(MadiMenu)
class MadiMenuAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_fa', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['title_en', 'title_fa', 'subtitle_en', 'subtitle_fa']
    inlines = []