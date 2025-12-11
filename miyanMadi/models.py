from django.conf import settings
from django.db import models
from core.models import BaseMenu, MenuItem


class MadiMenu(BaseMenu):
    """Main menu model for Madi"""
    
    service_hours = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Service Hours",
        help_text="e.g., 7:00 AM - 11:00 PM"
    )
    
    class Meta:
        db_table = 'madi_menu'
        verbose_name = "Madi Menu"
        verbose_name_plural = "Madi Menus"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title_en}"


class MadiMenuSection(models.Model):
    """Sections within Madi menu"""
    menu = models.ForeignKey(
        MadiMenu,
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
        db_table = 'madi_menu_section'
        verbose_name = "Madi Menu Section"
        verbose_name_plural = "Madi Menu Sections"
        ordering = ['display_order', 'created_at']
    
    def __str__(self):
        return f"{self.title_en}"


class MadiMenuItem(MenuItem):
    """Individual items in Madi menu sections"""
    section = models.ForeignKey(
        MadiMenuSection,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Menu Section"
    )
    
    class Meta:
        db_table = 'madi_menu_item'
        verbose_name = "Madi Menu Item"
        verbose_name_plural = "Madi Menu Items"
        ordering = ['display_order', 'created_at']


class MadiInventoryItem(models.Model):
    """Inventory item for Madi branch"""
    name = models.CharField(max_length=128)
    unit = models.CharField(max_length=32, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'madi_inventory_item'
        verbose_name = "Madi Inventory Item"
        verbose_name_plural = "Madi Inventory Items"

    def __str__(self):
        return self.name


class MadiInventoryRecord(models.Model):
    """Inventory record for Madi branch"""
    item = models.ForeignKey(
        MadiInventoryItem,
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
        db_table = 'madi_inventory_record'
        verbose_name = "Madi Inventory Record"
        verbose_name_plural = "Madi Inventory Records"
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.recorded_at.date()} {self.item.name} x{self.quantity}"
