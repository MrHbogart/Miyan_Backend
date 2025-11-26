from rest_framework import viewsets

from core.viewsets import AdminWritePermissionMixin
from .models import MiyanGallery
from .serializers import MiyanGallerySerializer


class MiyanGalleryViewSet(AdminWritePermissionMixin, viewsets.ModelViewSet):
    queryset = MiyanGallery.objects.all().order_by('order')
    serializer_class = MiyanGallerySerializer
