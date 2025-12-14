from django.contrib import admin

from . import models


@admin.register(models.Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')


@admin.register(models.Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'telegram_token', 'telegram_id', 'language_preference', 'created_at')
    search_fields = ('user__username', 'telegram_id', 'telegram_token')
    readonly_fields = ('telegram_token', 'created_at', 'updated_at')


@admin.register(models.StaffBranchAssignment)
class StaffBranchAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff', 'branch', 'is_primary', 'is_active', 'created_at')
    list_filter = ('is_primary', 'is_active', 'branch')
    search_fields = ('staff__user__username', 'branch__name')


@admin.register(models.StaffShift)
class StaffShiftAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff', 'branch', 'started_at', 'ended_at')
    list_filter = ('branch',)
    search_fields = ('staff__user__username',)


@admin.register(models.InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit', 'branch', 'is_active')
    list_filter = ('branch', 'is_active')
    search_fields = ('name',)


@admin.register(models.InventoryMeasurement)
class InventoryMeasurementAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'branch', 'quantity', 'measured_at', 'recorded_by')
    list_filter = ('branch', 'item')
    readonly_fields = ('measured_at',)


@admin.register(models.InventoryInput)
class InventoryInputAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'branch', 'quantity', 'recorded_at', 'recorded_by')
    list_filter = ('branch', 'item')
    readonly_fields = ('recorded_at',)


@admin.register(models.InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'branch', 'created_at', 'created_by')
    list_filter = ('branch', 'item')


@admin.register(models.MiyanGallery)
class MiyanGalleryAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'title_fa', 'order', 'created_at', 'updated_at')
    search_fields = ('title_en', 'title_fa')
