from rest_framework import serializers
from .models import MiyanGallery

class MiyanGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = MiyanGallery
        fields = '__all__'
