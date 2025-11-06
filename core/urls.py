from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'mian_beresht_menu1', views.MianBereshtMenu1ViewSet)
router.register(r'mian_beresht_menu2', views.MianBereshtMenu2ViewSet)
router.register(r'mian_madi_menu1', views.MianMadiMenu1ViewSet)
router.register(r'mian_madi_menu2', views.MianMadiMenu2ViewSet)
router.register(r'ingredients', views.IngredientViewSet)
router.register(r'recipes', views.RecipeViewSet)
router.register(r'sellrecords', views.SellRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
