from __future__ import annotations

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from core.models import TimeStampedModel


class BasicItem(TimeStampedModel):
    name = models.CharField(max_length=200, unique=True)
    unit = models.CharField(max_length=32)
    unit_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))],
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Basic Item'
        verbose_name_plural = 'Basic Items'

    def __str__(self) -> str:
        return self.name


class Recipe(TimeStampedModel):
    name = models.CharField(max_length=200, unique=True)
    price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))],
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self) -> str:
        return self.name


class RecipeIngredient(TimeStampedModel):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    basic_item = models.ForeignKey(
        BasicItem,
        on_delete=models.PROTECT,
        related_name='recipe_ingredients',
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.0001'))],
        help_text='Amount of the basic item used per recipe unit (in the same unit as the BasicItem).',
    )

    class Meta:
        unique_together = [('recipe', 'basic_item')]
        ordering = ['recipe__name', 'basic_item__name']
        verbose_name = 'Recipe Ingredient'
        verbose_name_plural = 'Recipe Ingredients'

    def __str__(self) -> str:
        return f'{self.recipe} -> {self.basic_item} ({self.amount} {self.basic_item.unit})'


class BranchBasicItemStock(TimeStampedModel):
    branch = models.ForeignKey(
        'miyanGroup.Branch',
        on_delete=models.CASCADE,
        related_name='basic_item_stocks',
    )
    item = models.ForeignKey(
        BasicItem,
        on_delete=models.CASCADE,
        related_name='branch_stocks',
    )
    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0'))],
        default=Decimal('0'),
    )

    class Meta:
        unique_together = [('branch', 'item')]
        ordering = ['branch__name', 'item__name']
        verbose_name = 'Branch Basic Item Stock'
        verbose_name_plural = 'Branch Basic Item Stock'

    def __str__(self) -> str:
        return f'{self.branch.code}: {self.item} = {self.quantity}'


class BranchRecipeStock(TimeStampedModel):
    branch = models.ForeignKey(
        'miyanGroup.Branch',
        on_delete=models.CASCADE,
        related_name='recipe_stocks',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='branch_stocks',
    )
    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0'))],
        default=Decimal('0'),
    )

    class Meta:
        unique_together = [('branch', 'recipe')]
        ordering = ['branch__name', 'recipe__name']
        verbose_name = 'Branch Recipe Stock'
        verbose_name_plural = 'Branch Recipe Stock'

    def __str__(self) -> str:
        return f'{self.branch.code}: {self.recipe} = {self.quantity}'


class InventoryAdjustment(TimeStampedModel):
    class ItemType(models.TextChoices):
        BASIC = 'basic', 'Basic Item'
        RECIPE = 'recipe', 'Recipe'

    class Mode(models.TextChoices):
        SET = 'set', 'Set'
        DELTA = 'delta', 'Delta'

    branch = models.ForeignKey(
        'miyanGroup.Branch',
        on_delete=models.CASCADE,
        related_name='inventory_adjustments',
    )
    item_type = models.CharField(max_length=16, choices=ItemType.choices)
    basic_item = models.ForeignKey(
        BasicItem,
        on_delete=models.PROTECT,
        related_name='inventory_adjustments',
        null=True,
        blank=True,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.PROTECT,
        related_name='inventory_adjustments',
        null=True,
        blank=True,
    )
    mode = models.CharField(max_length=16, choices=Mode.choices)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    stock_before = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0'))],
    )
    stock_after = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0'))],
    )
    note = models.CharField(max_length=255, blank=True)
    recorded_by = models.ForeignKey(
        'miyanGroup.Staff',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inventory_adjustments',
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Inventory Adjustment'
        verbose_name_plural = 'Inventory Adjustments'
        constraints = [
            models.CheckConstraint(
                name='inventory_adjustment_basic_item_matches_type',
                check=(
                    models.Q(item_type='basic', basic_item__isnull=False, recipe__isnull=True)
                    | models.Q(item_type='recipe', basic_item__isnull=True, recipe__isnull=False)
                ),
            ),
        ]

    def __str__(self) -> str:
        item = self.basic_item if self.item_type == self.ItemType.BASIC else self.recipe
        return f'{self.branch.code}: {self.mode} {item} ({self.quantity})'
