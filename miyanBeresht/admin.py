from django.contrib import admin
from .models import MiyanBereshtMenu

@admin.register(MiyanBereshtMenu)
class MiyanBereshtMenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available', 'created_at')
    list_filter = ('category', 'available')
    search_fields = ('name',)
