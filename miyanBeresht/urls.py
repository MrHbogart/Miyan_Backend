from rest_framework import routers
from .views import MiyanBereshtMenuViewSet

router = routers.DefaultRouter()
router.register(r'miyan_beresht_menu', MiyanBereshtMenuViewSet)

urlpatterns = router.urls
