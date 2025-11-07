from rest_framework import viewsets, permissions
from rest_framework.permissions import SAFE_METHODS
from . import models, serializers


# class IsStaffOrReadOnly(permissions.BasePermission):
#     """Allow read-only access for anyone, but restrict write operations to staff group members or superusers."""

#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return True
#         user = request.user
#         if not user or not user.is_authenticated:
#             return False
#         if user.is_superuser:
#             return True
#         return user.groups.filter(name='staff').exists()



# class IngredientViewSet(viewsets.ModelViewSet):
#     queryset = models.Ingredient.objects.all()
#     serializer_class = serializers.IngredientSerializer
#     permission_classes = (IsStaffOrReadOnly,)


# class RecipeViewSet(viewsets.ModelViewSet):
#     queryset = models.Recipe.objects.prefetch_related('ingredients')
#     serializer_class = serializers.RecipeSerializer
#     permission_classes = (IsStaffOrReadOnly,)


# class SellRecordViewSet(viewsets.ModelViewSet):
#     queryset = models.SellRecord.objects.select_related('sold_by')
#     serializer_class = serializers.SellRecordSerializer
#     permission_classes = (IsStaffOrReadOnly,)
