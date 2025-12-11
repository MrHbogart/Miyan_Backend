from django.contrib import admin
from .models import (
    BereshtMenu, BereshtMenuSection, BereshtMenuItem,
    BereshtInventoryItem, BereshtInventoryRecord
)


@admin.register(BereshtMenuItem)
class BereshtMenuItemAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'name_fa', 'section', 'price_fa', 'display_order']
    list_filter = ['section']
    search_fields = ['name_en', 'name_fa', 'description_en', 'description_fa']
    list_editable = ['price_fa', 'display_order']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name_fa', 'name_en', 'description_fa', 'description_en', 'section')
        }),
        ('Pricing', {
            'fields': ('price_fa', 'price_en')
        }),
        ('Media', {
            'fields': ('image', 'video')
        }),
        ('Organization', {
            'fields': ('display_order',)
        }),
    )


class BereshtMenuItemInline(admin.TabularInline):
    model = BereshtMenuItem
    extra = 1
    fields = ['name_en', 'name_fa', 'price_fa', 'image', 'video', 'display_order']


@admin.register(BereshtInventoryItem)
class BereshtInventoryItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit')
    search_fields = ('name',)


@admin.register(BereshtInventoryRecord)
class BereshtInventoryRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'recorded_at', 'item', 'quantity', 'recorded_by')
    list_filter = ('item',)
    readonly_fields = ('recorded_at',)



@admin.register(BereshtMenuSection)
class BereshtMenuSectionAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_fa', 'menu', 'display_order', 'is_active']
    list_filter = ['is_active', 'menu']
    inlines = [BereshtMenuItemInline]


@admin.register(BereshtMenu)
class BereshtMenuAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_fa', 'is_active', 'show_images', 'created_at']
    list_filter = ['is_active', 'show_images']
    inlines = []
