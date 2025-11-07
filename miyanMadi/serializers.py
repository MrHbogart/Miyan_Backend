from rest_framework import serializers
from .models import MiyanMadiMenu

class MiyanMadiMenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = MiyanMadiMenu
        fields = ['id', 'name_fa', 'name_en', 'subtitle_fa', \
                  'subtitle_en', 'category', 'price', 'available', \
                    'image', 'created_at', 'updated_at']

