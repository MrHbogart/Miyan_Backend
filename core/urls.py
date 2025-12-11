from django.urls import include, path
from rest_framework import routers

from .views import HealthcheckView, StaffLinkAPIView, TokenByTelegramAPIView, StaffProfileViewSet

router = routers.DefaultRouter()
router.register(r'staff', StaffProfileViewSet, basename='staff-profile')

urlpatterns = [
    path('health/', HealthcheckView.as_view(), name='core-health'),
    path('staff/link/', StaffLinkAPIView.as_view(), name='staff-link'),
    path('staff/get-token/', TokenByTelegramAPIView.as_view(), name='get-token'),
