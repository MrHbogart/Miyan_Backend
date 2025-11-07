from django.contrib import admin
from .models import MiyanGallery

@admin.register(MiyanGallery)
class MiyanGalleryAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'title_fa', 'order', 'created_at', 'image')
    ordering = ('order',)
