from django.contrib import admin
from .models import MiyanBereshtMenu

@admin.register(MiyanBereshtMenu)
class MiyanBereshtMenuAdmin(admin.ModelAdmin):
    list_display = ('name_fa', 'name_en', 'category', 'price', 'subtitle_fa', 'subtitle_en', 'available', 'created_at', 'image')
    list_filter = ('category', 'available')
    search_fields = ('name_en','name_fa')