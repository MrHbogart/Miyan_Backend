"""Reusable DRF mixins to keep the API surface consistent."""

from __future__ import annotations

from rest_framework import permissions, status
from rest_framework.response import Response


class AdminWritePermissionMixin:
    """Allow anonymous/any authenticated reads while locking writes to admins."""

    admin_write_actions = {'create', 'update', 'partial_update', 'destroy'}
    read_permission_class = permissions.AllowAny
    write_permission_class = permissions.IsAdminUser

    def get_permissions(self):
        action = getattr(self, 'action', None)
        if action in self.admin_write_actions:
            permission_classes = [self.write_permission_class]
        else:
            permission_classes = [self.read_permission_class]
        return [permission() for permission in permission_classes]


class MenuTypeActionMixin:
    """Helper utilities for menu viewsets that expose custom endpoints."""

    menu_not_found_message = 'No active menu found'

    def _menu_queryset(self):
        return self.filter_queryset(self.get_queryset())

    def _get_menu_for_type(self, menu_type: str):
        return self._menu_queryset().filter(menu_type=menu_type).first()

    def respond_with_menu_type(
        self,
        menu_type: str,
        *,
        fallback_first: bool = False,
        not_found_message: str | None = None,
    ) -> Response:
        menu = self._get_menu_for_type(menu_type)
        if not menu and fallback_first:
            menu = self._menu_queryset().first()
        if not menu:
            message = not_found_message or self.menu_not_found_message
            return Response({'detail': message}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(menu)
        return Response(serializer.data)

    def list_active_menus(self) -> Response:
        queryset = self._menu_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
