from django.db import models
from core.models import BaseMenu, MenuItem
from miyanGroup.models import Branch


class BereshtMenu(BaseMenu):
    """Main menu model for Beresht"""
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='beresht_menus')
    
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

