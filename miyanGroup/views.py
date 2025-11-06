from rest_framework import viewsets
from .models import MiyanGallery
from .serializers import MiyanGallerySerializer

class MiyanGalleryViewSet(viewsets.ModelViewSet):
    queryset = MiyanGallery.objects.all()
    serializer_class = MiyanGallerySerializer
    permission_classes = []
