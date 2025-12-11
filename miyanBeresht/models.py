from django.conf import settings
from django.db import models
from core.models import BaseMenu, MenuItem


class BereshtMenu(BaseMenu):
    """Main menu model for Beresht"""
    
    class Meta:
        db_table = 'beresht_menu'
        verbose_name = "Beresht Menu"
        verbose_name_plural = "Beresht Menus"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title_en}"


class BereshtMenuItem(MenuItem):
    """Individual items in Beresht menu sections"""
    section = models.ForeignKey(
        'BereshtMenuSection',
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Menu Section"
    )
    
    class Meta:
        db_table = 'beresht_menu_item'
        verbose_name = "Beresht Menu Item"
        verbose_name_plural = "Beresht Menu Items"
        ordering = ['display_order', 'created_at']


class BereshtMenuSection(models.Model):
    """Sections within Beresht menu"""
    menu = models.ForeignKey(
        BereshtMenu,
        on_delete=models.CASCADE,
        related_name='sections',
        verbose_name="Parent Menu"
    )
    
    title_fa = models.CharField(max_length=255, verbose_name="Section Title (Persian)")
    title_en = models.CharField(max_length=255, verbose_name="Section Title (English)")
    description_fa = models.TextField(blank=True, null=True, verbose_name="Description (Persian)")
    description_en = models.TextField(blank=True, null=True, verbose_name="Description (English)")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'beresht_menu_section'
        verbose_name = "Beresht Menu Section"
        verbose_name_plural = "Beresht Menu Sections"
        ordering = ['display_order', 'created_at']
    
    def __str__(self):
        return f"{self.title_en}"


class BereshtInventoryItem(models.Model):
    """Inventory item for Beresht branch"""
    name = models.CharField(max_length=128)
    unit = models.CharField(max_length=32, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'beresht_inventory_item'
        verbose_name = "Beresht Inventory Item"
        verbose_name_plural = "Beresht Inventory Items"

    def __str__(self):
        return self.name


class BereshtInventoryRecord(models.Model):
    """Inventory record for Beresht branch"""
    item = models.ForeignKey(
        BereshtInventoryItem,
        on_delete=models.CASCADE,
        related_name='records'
    )
    quantity = models.IntegerField()
    note = models.TextField(blank=True)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'beresht_inventory_record'
        verbose_name = "Beresht Inventory Record"
        verbose_name_plural = "Beresht Inventory Records"
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.recorded_at.date()} {self.item.name} x{self.quantity}"
