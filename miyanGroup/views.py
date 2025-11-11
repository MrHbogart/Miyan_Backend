from rest_framework import viewsets, permissions
from .models import MiyanGallery
from .serializers import MiyanGallerySerializer

class MiyanGalleryViewSet(viewsets.ModelViewSet):
    queryset = MiyanGallery.objects.all().order_by('order')
    serializer_class = MiyanGallerySerializer

    def get_permissions(self):
        # Allow anyone to read (GET, HEAD, OPTIONS). Only admin users can create/update/delete.
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
