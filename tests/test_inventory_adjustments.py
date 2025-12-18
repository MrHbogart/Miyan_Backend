from decimal import Decimal

import pytest
from rest_framework import serializers as drf_serializers

from inventory import models, serializers
from miyanGroup.models import Branch, Staff

pytestmark = pytest.mark.django_db


def test_adjustment_sets_branch_stock(django_user_model):
    branch = Branch.objects.create(name='Beresht', code='beresht')
    item = models.BasicItem.objects.create(name='Sugar', unit='kg', unit_price=Decimal('10'))
    user = django_user_model.objects.create_user(username='worker', password='pass')
    staff = Staff.objects.create(user=user)

    serializer = serializers.InventoryAdjustmentSerializer(
        data={
            'branch_id': branch.id,
            'item_type': models.InventoryAdjustment.ItemType.BASIC,
            'basic_item': item.id,
            'mode': models.InventoryAdjustment.Mode.SET,
            'quantity': '5',
        }
    )
    serializer.is_valid(raise_exception=True)
    adjustment = serializer.save(branch=branch, recorded_by=staff)

    stock = models.BranchBasicItemStock.objects.get(branch=branch, item=item)
    assert stock.quantity == Decimal('5')
    assert adjustment.stock_before == Decimal('0')
    assert adjustment.stock_after == Decimal('5')
    assert adjustment.recorded_by == staff


def test_adjustment_rejects_negative_result(django_user_model):
    branch = Branch.objects.create(name='Madi', code='madi')
    item = models.BasicItem.objects.create(name='Milk', unit='litre', unit_price=Decimal('5'))
    models.BranchBasicItemStock.objects.create(branch=branch, item=item, quantity=Decimal('2'))

    serializer = serializers.InventoryAdjustmentSerializer(
        data={
            'branch_id': branch.id,
            'item_type': models.InventoryAdjustment.ItemType.BASIC,
            'basic_item': item.id,
            'mode': models.InventoryAdjustment.Mode.DELTA,
            'quantity': '-5',
        }
    )
    serializer.is_valid(raise_exception=True)
    with pytest.raises(drf_serializers.ValidationError):
        serializer.save(branch=branch)
