from rest_framework import serializers
from .models import MiyanBereshtMenu

class MiyanBereshtMenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = MiyanBereshtMenu
        fields = ['id', 'name_fa', 'name_en', 'subtitle_fa', \
                  'subtitle_en', 'category', 'price', 'available', \
                    'image', 'created_at', 'updated_at']

