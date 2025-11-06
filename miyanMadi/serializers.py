from rest_framework import serializers
from .models import MiyanMadiMenu

class MiyanMadiMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiyanMadiMenu
        fields = '__all__'
