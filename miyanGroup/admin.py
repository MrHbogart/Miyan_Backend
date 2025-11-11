from django.contrib import admin
from .models import MiyanGallery

@admin.register(MiyanGallery)
class MiyanGalleryAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_fa', 'display_order']
    search_fields = ['title_en', 'title_fa', 'display_order']



