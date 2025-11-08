from django.contrib import admin
from .models import MiyanMadiMenu

@admin.register(MiyanMadiMenu)
class MiyanMadiMenuAdmin(admin.ModelAdmin):
    list_display = ('name_fa', 'name_en', 'category', 'price', 'subtitle_fa', 'subtitle_en', 'available', 'created_at', 'image')
    list_filter = ('category', 'available')
    search_fields = ('name',)