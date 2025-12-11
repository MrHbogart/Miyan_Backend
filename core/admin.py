from django.contrib import admin
from . import models


@admin.register(models.StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bot_token', 'telegram_id', 'created_at')
    readonly_fields = ('bot_token', 'created_at', 'updated_at')
    search_fields = ('user__username', 'telegram_id')
