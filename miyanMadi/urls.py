from rest_framework import routers
from .views import MiyanMadiMenuViewSet

router = routers.DefaultRouter()
router.register(r'miyan_madi_menu', MiyanMadiMenuViewSet)

urlpatterns = router.urls
