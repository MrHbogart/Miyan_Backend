from django.contrib import admin
from . import models


@admin.register(models.Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location')


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit')


@admin.register(models.StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bot_token', 'telegram_id')
    readonly_fields = ('bot_token',)


@admin.register(models.InventoryRecord)
class InventoryRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'recorded_at', 'branch', 'item', 'quantity', 'recorded_by')
    list_filter = ('branch', 'item')
