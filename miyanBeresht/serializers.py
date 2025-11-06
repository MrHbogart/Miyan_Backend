from rest_framework import serializers
from .models import MiyanBereshtMenu

class MiyanBereshtMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiyanBereshtMenu
        fields = '__all__'
