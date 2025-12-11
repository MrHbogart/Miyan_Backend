from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'records', views.InventoryRecordViewSet, basename='inventoryrecord')
router.register(r'branches', views.BranchViewSet, basename='branch')
router.register(r'items', views.ItemViewSet, basename='item')

urlpatterns = [
    path('staff/link/', views.StaffLinkAPIView.as_view(), name='staff-link'),
    path('get-token/', views.TokenByTelegramAPIView.as_view(), name='get-token'),
    path('', include(router.urls)),
]
