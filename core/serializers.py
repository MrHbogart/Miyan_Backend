"""Shared serializer primitives used across the project."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any, Mapping

from rest_framework import serializers

DEFAULT_MENU_IMAGE = '/images/medium/default-menu.jpg'
DEFAULT_TODAYS_TITLE = {'fa': 'آیتم‌های تازه امروز', 'en': "Today's Fresh"}
DEFAULT_TODAYS_SECTION_TITLE = {'fa': 'پیشنهاد امروز', 'en': "Today's Special"}


def _format_decimal_string(value: Decimal) -> str:
    as_string = format(value, 'f')
    if '.' in as_string:
        as_string = as_string.rstrip('0').rstrip('.')
    return as_string


def _coerce_decimal(value: Any) -> Decimal | None:
    if value in (None, ''):
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None


def format_price_display(value: Any, fallback: str | None, lang: str) -> str:
    """Normalize price display strings for the frontend payload."""
    fallback = fallback or ''
    decimal_value = _coerce_decimal(value)
    if decimal_value is None:
        return fallback or (str(value) if value not in (None, '') else '')

    thousands = decimal_value / Decimal('1000')
    formatted = _format_decimal_string(thousands)
    if lang == 'fa':
        return formatted
    return f"IRR {formatted}"


def build_menu_item_payload(
    item_data: Mapping[str, Any],
    *,
    default_image: str = DEFAULT_MENU_IMAGE,
) -> dict[str, Any]:
    """Transform nested item serializer output to the public representation."""
    # Only use the formatted price fields provided by the models.
    image = default_image
    return {
        'name': {'fa': item_data.get('name_fa'), 'en': item_data.get('name_en')},
        'description': {
            'fa': item_data.get('description_fa') or '',
            'en': item_data.get('description_en') or '',
        },
        'price': {
            'fa': item_data.get('price_fa') or '',
            'en': item_data.get('price_en') or '',
        },
        'image': image,
    }


def _subtitle_payload(subtitle_fa: str | None, subtitle_en: str | None):
    if subtitle_fa or subtitle_en:
        return {'fa': subtitle_fa, 'en': subtitle_en}
    return None


def transform_menu_payload(
    menu_data: Mapping[str, Any],
    *,
    todays_title: Mapping[str, str] = DEFAULT_TODAYS_TITLE,
    todays_section_title: Mapping[str, str] = DEFAULT_TODAYS_SECTION_TITLE,
    default_image: str = DEFAULT_MENU_IMAGE,
    include_todays: bool = True,
) -> dict[str, Any]:
    """Convert internal serializer data into the public API contract."""
    sections_out: list[dict[str, Any]] = []

    for section in menu_data.get('sections') or []:
        if not section.get('is_active'):
            continue

        section_items = []
        for item in section.get('items') or []:
            # include all items; availability flags removed to simplify model
            section_items.append(build_menu_item_payload(item, default_image=default_image))

        sections_out.append(
            {
                'title': {'fa': section.get('title_fa'), 'en': section.get('title_en')},
                'items': section_items,
            }
        )

    payload: dict[str, Any] = {
        'title': {'fa': menu_data.get('title_fa'), 'en': menu_data.get('title_en')},
        'subtitle': _subtitle_payload(
            menu_data.get('subtitle_fa'), menu_data.get('subtitle_en')
        ),
        'sections': sections_out,
    }

    # Today's special aggregation removed — frontend will not receive a separate 'todays' section

    return payload


class MenuPresentationSerializer(serializers.ModelSerializer):
    """Base serializer that exposes menus in the shape expected by the frontend."""

    todays_title: Mapping[str, str] = DEFAULT_TODAYS_TITLE
    todays_section_title: Mapping[str, str] = DEFAULT_TODAYS_SECTION_TITLE
    include_todays: bool = True
    default_image: str = DEFAULT_MENU_IMAGE

    def get_extra_payload(
        self,
        instance,
        serialized_data: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        """Allow subclasses to inject brand-specific metadata."""
        return {}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        payload = transform_menu_payload(
            data,
            todays_title=self.todays_title,
            todays_section_title=self.todays_section_title,
            default_image=self.default_image,
            include_todays=self.include_todays,
        )

        extra = self.get_extra_payload(instance, data)
        if extra:
            payload.update(extra)
        return payload
