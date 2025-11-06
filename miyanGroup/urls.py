from rest_framework import routers
from .views import MiyanGalleryViewSet

router = routers.DefaultRouter()
router.register(r'miyan_gallery', MiyanGalleryViewSet)

urlpatterns = router.urls
