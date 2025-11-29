"""Reusable DRF mixins and base viewsets for a consistent API surface."""

from __future__ import annotations

import logging

from django.db.models import QuerySet
from django.db.utils import ProgrammingError
from django.core.exceptions import FieldError
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

logger = logging.getLogger(__name__)


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


class PublicQuerysetMixin:
    """Filter read-only actions to public records while keeping admin access."""

    public_filter_field: str | None = None
    public_filter_value: bool = True
    staff_bypass_public_filter: bool = True

    def is_write_action(self) -> bool:
        return getattr(self, 'action', None) in getattr(
            self, 'admin_write_actions', set()
        )

    def should_filter_public_queryset(self) -> bool:
        if not self.public_filter_field:
            return False
        if self.is_write_action():
            return False
        if (
            self.staff_bypass_public_filter
            and getattr(self.request, 'user', None) is not None
            and self.request.user.is_staff
        ):
            return False
        return True

    def filter_queryset_for_public(self, queryset: QuerySet) -> QuerySet:
        if not self.should_filter_public_queryset():
            return queryset
        return queryset.filter(
            **{self.public_filter_field: self.public_filter_value}
        )

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        return self.filter_queryset_for_public(queryset)


class SafeQuerysetMixin:
    """Wrap database access so missing tables don't crash the API."""

    def get_queryset(self) -> QuerySet:
        try:
            return super().get_queryset()
        except ProgrammingError:
            logger.warning('Missing database table while resolving %s', self.__class__.__name__, exc_info=True)
            return self.queryset.none()


class MenuTypeActionMixin:
    """Helper utilities for menu viewsets that expose custom endpoints."""

    menu_not_found_message = 'No active menu found'

    def _menu_queryset(self):
        return self.filter_queryset(self.get_queryset())

    def _get_menu_for_type(self, menu_type: str):
        # Try to filter by `menu_type` if the field exists; otherwise return first menu.
        try:
            return self._menu_queryset().filter(menu_type=menu_type).first()
        except (FieldError, Exception):
            return self._menu_queryset().first()

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


class BaseMenuViewSet(
    AdminWritePermissionMixin,
    SafeQuerysetMixin,
    PublicQuerysetMixin,
    MenuTypeActionMixin,
    viewsets.ModelViewSet,
):
    """Shared behaviors for brand-specific menu viewsets."""

    public_filter_field = 'is_active'
    main_menu_not_found_message = 'No active menu found'
    todays_not_found_message = "No today's special menu found"

    @action(detail=False, methods=['get'])
    def main(self, request):
        """Public endpoint for the active main menu."""
        return self.respond_with_menu_type(
            'main',
            fallback_first=True,
            not_found_message=self.main_menu_not_found_message,
        )

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Public endpoint for today's specials."""
        return self.respond_with_menu_type(
            'today',
            not_found_message=self.todays_not_found_message,
        )

    @action(detail=False, methods=['get'])
    def all(self, request):
        """Return all active menus for the brand."""
        return self.list_active_menus()


class BaseMenuItemViewSet(
    AdminWritePermissionMixin,
    SafeQuerysetMixin,
    PublicQuerysetMixin,
    viewsets.ModelViewSet,
):
    """Base class for menu items that exposes the common public actions."""

    public_filter_field = None

    def _special_response(self, **filters):
        try:
            queryset = self.filter_queryset(self.get_queryset().filter(**filters))
        except FieldError:
            queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Public endpoint for featured items."""
        return self._special_response(is_featured=True)

    @action(detail=False, methods=['get'])
    def todays_specials(self, request):
        """Public endpoint for today's specials."""
        return self._special_response(is_todays_special=True)