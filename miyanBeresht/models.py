# miyanBeresht/models.py
from django.db import models
from core.models import BaseMenu, MenuSection, MenuItem

class BereshtMenu(BaseMenu):
    """Main menu model for Beresht that matches frontend structure exactly"""
    
    # Menu type classification
    MENU_TYPE_CHOICES = [
        ('main', 'Main Menu'),
        ('today', "Today's Specials"),
        ('seasonal', 'Seasonal Menu'),
        ('promotional', 'Promotional Menu'),
    ]
    
    menu_type = models.CharField(
        max_length=20,
        choices=MENU_TYPE_CHOICES,
        default='main',
        verbose_name="Menu Type"
    )
    
    # Additional menu-level fields
    cover_image = models.ImageField(
        upload_to='menu_covers/%Y/%m/%d/', 
        blank=True, 
        null=True,
        verbose_name="Menu Cover Image"
    )
    
    # Validity period for time-sensitive menus
    valid_from = models.DateTimeField(
        blank=True, 
        null=True,
        verbose_name="Valid From"
    )
    valid_until = models.DateTimeField(
        blank=True, 
        null=True,
        verbose_name="Valid Until"
    )
    
    class Meta:
        db_table = 'beresht_menu'
        verbose_name = "Beresht Menu"
        verbose_name_plural = "Beresht Menus"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title_en} ({self.get_menu_type_display()})"


class BereshtMenuSection(MenuSection):
    """Sections within Beresht menu (Espresso Based, Milk Based, etc.)"""
    menu = models.ForeignKey(
        BereshtMenu,
        on_delete=models.CASCADE,
        related_name='sections',
        verbose_name="Parent Menu"
    )
    
    # Section-specific fields
    section_type = models.CharField(
        max_length=50,
        choices=[
            ('beverages', 'Beverages'),
            ('food', 'Food Items'),
            ('desserts', 'Desserts'),
            ('specials', 'Specials'),
        ],
        default='beverages',
        verbose_name="Section Type"
    )
    
    class Meta:
        db_table = 'beresht_menu_section'
        verbose_name = "Beresht Menu Section"
        verbose_name_plural = "Beresht Menu Sections"
        ordering = ['display_order', 'created_at']


class BereshtMenuItem(MenuItem):
    """Individual items in Beresht menu sections"""
    section = models.ForeignKey(
        BereshtMenuSection,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Menu Section"
    )
    
    # Coffee/restaurant specific fields
    COFFEE_TYPE_CHOICES = [
        ('espresso', 'Espresso Based'),
        ('milk', 'Milk Based'),
        ('filter', 'Filter Coffee'),
        ('tea', 'Tea & Infusions'),
        ('specialty', 'Specialty Drinks'),
        ('food', 'Food Items'),
        ('dessert', 'Desserts'),
    ]
    
    item_type = models.CharField(
        max_length=20,
        choices=COFFEE_TYPE_CHOICES,
        default='espresso',
        verbose_name="Item Type"
    )
    
    # Additional restaurant-specific fields
    ingredients_fa = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Ingredients (Persian)"
    )
    ingredients_en = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Ingredients (English)"
    )
    
    # Size options (if applicable)
    available_sizes = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Available Sizes",
        help_text="Comma-separated sizes (e.g., Small,Medium,Large)"
    )
    
    # Spice level (for food items)
    spice_level = models.PositiveIntegerField(
        default=0,
        verbose_name="Spice Level",
        help_text="0-5, where 0 is not spicy and 5 is very spicy"
    )
    
    class Meta:
        db_table = 'beresht_menu_item'
        verbose_name = "Beresht Menu Item"
        verbose_name_plural = "Beresht Menu Items"
        ordering = ['display_order', 'created_at']
    
    def get_available_sizes_list(self):
        """Return available sizes as a list"""
        if self.available_sizes:
            return [size.strip() for size in self.available_sizes.split(',')]
        return []