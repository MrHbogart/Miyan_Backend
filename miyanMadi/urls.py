from rest_framework import routers
from .views import MiyanMadiMenuViewSet

router = routers.DefaultRouter()
router.register(r'miyan_beresht_menu', MiyanMadiMenuViewSet)

urlpatterns = router.urls
