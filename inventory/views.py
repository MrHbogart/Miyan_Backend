from __future__ import annotations

from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from core.viewsets import AdminWritePermissionMixin
from miyanGroup.models import Staff
from . import models, serializers


class StaffBranchMixin:
    """Shared helpers for resolving the requesting staff and active branch."""

    def _get_staff_or_error(self) -> Staff:
        try:
            return self.request.user.staff_profile
        except Staff.DoesNotExist:
            raise PermissionDenied('Staff profile required.')

    def _get_active_branch_or_error(self):
        staff = self._get_staff_or_error()
        active_shift = staff.active_shift
        if not active_shift:
            raise PermissionDenied('Active shift required.')
        return active_shift.branch, staff


class BasicItemViewSet(AdminWritePermissionMixin, viewsets.ModelViewSet):
    queryset = models.BasicItem.objects.all()
    serializer_class = serializers.BasicItemSerializer
    admin_write_actions = {'create', 'update', 'partial_update', 'destroy'}
    read_permission_class = permissions.IsAuthenticated
    write_permission_class = permissions.IsAdminUser


class RecipeViewSet(AdminWritePermissionMixin, viewsets.ModelViewSet):
    queryset = models.Recipe.objects.prefetch_related('ingredients__basic_item').all()
    serializer_class = serializers.RecipeSerializer
    admin_write_actions = {'create', 'update', 'partial_update', 'destroy'}
    read_permission_class = permissions.IsAuthenticated
    write_permission_class = permissions.IsAdminUser


class BranchBasicItemStockViewSet(StaffBranchMixin, AdminWritePermissionMixin, viewsets.ModelViewSet):
    queryset = models.BranchBasicItemStock.objects.select_related('branch', 'item').all()
    serializer_class = serializers.BranchBasicItemStockSerializer
    admin_write_actions = {'create', 'update', 'partial_update', 'destroy'}
    read_permission_class = permissions.IsAuthenticated
    write_permission_class = permissions.IsAdminUser

    def get_queryset(self):
        queryset = super().get_queryset()
        branch_param = self.request.query_params.get('branch')
        if self.request.user.is_staff:
            if branch_param:
                queryset = queryset.filter(branch_id=branch_param)
            return queryset

        active_branch, _ = self._get_active_branch_or_error()
        if branch_param and str(branch_param) != str(active_branch.id):
            raise PermissionDenied('Branch mismatch for active shift.')
        return queryset.filter(branch=active_branch)


class BranchRecipeStockViewSet(StaffBranchMixin, AdminWritePermissionMixin, viewsets.ModelViewSet):
    queryset = models.BranchRecipeStock.objects.select_related('branch', 'recipe').all()
    serializer_class = serializers.BranchRecipeStockSerializer
    admin_write_actions = {'create', 'update', 'partial_update', 'destroy'}
    read_permission_class = permissions.IsAuthenticated
    write_permission_class = permissions.IsAdminUser

    def get_queryset(self):
        queryset = super().get_queryset()
        branch_param = self.request.query_params.get('branch')
        if self.request.user.is_staff:
            if branch_param:
                queryset = queryset.filter(branch_id=branch_param)
            return queryset

        active_branch, _ = self._get_active_branch_or_error()
        if branch_param and str(branch_param) != str(active_branch.id):
            raise PermissionDenied('Branch mismatch for active shift.')
        return queryset.filter(branch=active_branch)


class InventoryAdjustmentViewSet(StaffBranchMixin, viewsets.ModelViewSet):
    queryset = models.InventoryAdjustment.objects.select_related(
        'branch', 'basic_item', 'recipe', 'recorded_by'
    ).all()
    serializer_class = serializers.InventoryAdjustmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        branch_param = self.request.query_params.get('branch')

        if self.request.user.is_staff:
            if branch_param:
                queryset = queryset.filter(branch_id=branch_param)
            return queryset

        try:
            active_branch, _ = self._get_active_branch_or_error()
        except PermissionDenied:
            return queryset.none()

        return queryset.filter(branch=active_branch)

    def perform_create(self, serializer):
        staff = None
        branch = serializer.validated_data.get('branch')

        if self.request.user.is_staff:
            if not branch:
                raise PermissionDenied('Branch is required for adjustments.')
        else:
            branch, staff = self._get_active_branch_or_error()
            if serializer.validated_data.get('branch') and serializer.validated_data['branch'] != branch:
                raise PermissionDenied('Branch mismatch for active shift.')

        serializer.save(branch=branch, recorded_by=staff)
