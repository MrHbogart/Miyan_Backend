from rest_framework import viewsets, permissions
from .models import MiyanBereshtMenu
from .serializers import MiyanBereshtMenuSerializer

class MiyanBereshtMenuViewSet(viewsets.ModelViewSet):
    queryset = MiyanBereshtMenu.objects.all().order_by('id')
    serializer_class = MiyanBereshtMenuSerializer
    permission_classes = [permissions.AllowAny]
