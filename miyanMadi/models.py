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
    is_main_section = models.BooleanField(
        default=True,
        verbose_name="Is Main Section",
        help_text="Mark false for side item groupings like add-ons or syrups.",
    )
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
