from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'basic-items', views.BasicItemViewSet, basename='basic-item')
router.register(r'recipes', views.RecipeViewSet, basename='recipe')
router.register(r'branch-basic-stock', views.BranchBasicItemStockViewSet, basename='branch-basic-stock')
router.register(r'branch-recipe-stock', views.BranchRecipeStockViewSet, basename='branch-recipe-stock')
router.register(r'adjustments', views.InventoryAdjustmentViewSet, basename='inventory-adjustment')

urlpatterns = router.urls
