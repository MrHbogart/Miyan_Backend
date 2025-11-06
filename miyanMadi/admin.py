from django.contrib import admin
from .models import MiyanMadiMenu

@admin.register(MiyanMadiMenu)
class MiyanMadiMenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available', 'created_at')
    list_filter = ('category', 'available')
    search_fields = ('name',)
