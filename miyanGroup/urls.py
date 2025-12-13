from django.urls import path, include
from rest_framework import routers
from .views import MiyanGalleryViewSet
from core.views import StaffLinkAPIView, TokenByTelegramAPIView, StaffProfileViewSet

router = routers.DefaultRouter()
router.register(r'miyan_gallery', MiyanGalleryViewSet)
router.register(r'staff', StaffProfileViewSet, basename='staff-profile')

urlpatterns = [
	path('', include(router.urls)),
	path('staff/link/', StaffLinkAPIView.as_view(), name='group-staff-link'),
	path('staff/get-token/', TokenByTelegramAPIView.as_view(), name='group-get-token'),
]
