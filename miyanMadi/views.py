from rest_framework import viewsets, permissions
from .models import MiyanMadiMenu
from .serializers import MiyanMadiMenuSerializer

class MiyanMadiMenuViewSet(viewsets.ModelViewSet):
    queryset = MiyanMadiMenu.objects.all().order_by('id')
    serializer_class = MiyanMadiMenuSerializer
    permission_classes = [permissions.AllowAny]  # change to IsAuthenticated for admin-only
