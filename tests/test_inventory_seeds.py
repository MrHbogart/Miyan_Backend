from decimal import Decimal

import pytest
from django.core.management import call_command

from inventory.management.commands.seed_inventory_items import INVENTORY_ITEMS
from inventory.models import BasicItem

pytestmark = pytest.mark.django_db


def test_seed_inventory_items_creates_and_updates_curated_list():
    call_command('seed_inventory_items')

    assert BasicItem.objects.count() == len(INVENTORY_ITEMS)
    lemon_juice = BasicItem.objects.get(name='آبلیمو')
    assert lemon_juice.unit == '1 لیتری'
    assert lemon_juice.unit_price == Decimal('305000')

    lemon_juice.unit = 'changed unit'
    lemon_juice.unit_price = Decimal('1')
    lemon_juice.save()

    call_command('seed_inventory_items')
    lemon_juice.refresh_from_db()
    assert lemon_juice.unit == '1 لیتری'
    assert lemon_juice.unit_price == Decimal('305000')
    assert BasicItem.objects.count() == len(INVENTORY_ITEMS)


def test_seed_inventory_items_prunes_missing_when_requested():
    call_command('seed_inventory_items')
    stray = BasicItem.objects.create(name='Test Item', unit='u', unit_price=Decimal('5'))

    call_command('seed_inventory_items', prune_missing=True)

    assert not BasicItem.objects.filter(id=stray.id).exists()
    assert BasicItem.objects.count() == len(INVENTORY_ITEMS)
