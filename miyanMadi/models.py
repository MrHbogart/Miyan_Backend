# miyanMadi/models.py
from django.db import models
from core.models import BaseMenu, MenuSection, MenuItem

class MadiMenu(BaseMenu):
    """Main menu model for Madi that matches frontend structure exactly"""
    
    # Menu type classification
    MENU_TYPE_CHOICES = [
        ('main', 'Main Menu'),
        ('today', "Today's Specials"),
        ('seasonal', 'Seasonal Menu'),
        ('promotional', 'Promotional Menu'),
        ('breakfast', 'Breakfast Menu'),
        ('lunch', 'Lunch Menu'),
        ('dinner', 'Dinner Menu'),
    ]
    
    menu_type = models.CharField(
        max_length=20,
        choices=MENU_TYPE_CHOICES,
        default='main',
        verbose_name="Menu Type"
    )
    
    # Additional menu-level fields
    cover_image = models.ImageField(
        upload_to='madi_menu_covers/%Y/%m/%d/', 
        blank=True, 
        null=True,
        verbose_name="Menu Cover Image"
    )
    
    # Restaurant-specific settings
    service_hours = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Service Hours",
        help_text="e.g., 7:00 AM - 11:00 PM"
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
        db_table = 'madi_menu'
        verbose_name = "Madi Menu"
        verbose_name_plural = "Madi Menus"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title_en} ({self.get_menu_type_display()})"


class MadiMenuSection(MenuSection):
    """Sections within Madi menu"""
    menu = models.ForeignKey(
        MadiMenu,
        on_delete=models.CASCADE,
        related_name='sections',
        verbose_name="Parent Menu"
    )
    
    # Section-specific fields
    section_type = models.CharField(
        max_length=50,
        choices=[
            ('appetizers', 'Appetizers'),
            ('main_courses', 'Main Courses'),
            ('sides', 'Side Dishes'),
            ('desserts', 'Desserts'),
            ('beverages', 'Beverages'),
            ('specials', 'Daily Specials'),
            ('breakfast', 'Breakfast Items'),
        ],
        default='main_courses',
        verbose_name="Section Type"
    )
    
    # Meal type classification
    meal_type = models.CharField(
        max_length=20,
        choices=[
            ('breakfast', 'Breakfast'),
            ('lunch', 'Lunch'),
            ('dinner', 'Dinner'),
            ('any', 'Any Time'),
        ],
        default='any',
        verbose_name="Meal Type"
    )
    
    class Meta:
        db_table = 'madi_menu_section'
        verbose_name = "Madi Menu Section"
        verbose_name_plural = "Madi Menu Sections"
        ordering = ['display_order', 'created_at']


class MadiMenuItem(MenuItem):
    """Individual items in Madi menu sections"""
    section = models.ForeignKey(
        MadiMenuSection,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Menu Section"
    )
    
    # Restaurant-specific fields
    ITEM_TYPE_CHOICES = [
        ('appetizer', 'Appetizer'),
        ('main_course', 'Main Course'),
        ('side_dish', 'Side Dish'),
        ('dessert', 'Dessert'),
        ('beverage', 'Beverage'),
        ('breakfast', 'Breakfast Item'),
        ('salad', 'Salad'),
        ('soup', 'Soup'),
        ('sandwich', 'Sandwich'),
        ('pasta', 'Pasta'),
        ('seafood', 'Seafood'),
        ('grill', 'Grill'),
    ]
    
    item_type = models.CharField(
        max_length=20,
        choices=ITEM_TYPE_CHOICES,
        default='main_course',
        verbose_name="Item Type"
    )
    
    # Cuisine type
    cuisine_type = models.CharField(
        max_length=50,
        choices=[
            ('persian', 'Persian'),
            ('international', 'International'),
            ('mediterranean', 'Mediterranean'),
            ('asian', 'Asian'),
            ('fusion', 'Fusion'),
            ('iranian', 'Iranian Traditional'),
        ],
        default='persian',
        verbose_name="Cuisine Type"
    )
    
    # Ingredients
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
    
    # Cooking and serving information
    cooking_method = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Cooking Method",
        help_text="e.g., Grilled, Fried, Baked"
    )
    
    serving_temperature = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Serving Temperature",
        help_text="e.g., Hot, Cold, Warm"
    )
    
    # Spice level
    spice_level = models.PositiveIntegerField(
        default=0,
        verbose_name="Spice Level",
        help_text="0-5, where 0 is not spicy and 5 is very spicy"
    )
    
    # Portion information
    portion_size = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Portion Size",
        help_text="e.g., 300g, Regular, Large"
    )
    
    # Chef's recommendation
    is_chefs_special = models.BooleanField(
        default=False,
        verbose_name="Chef's Special"
    )
    
    # Popularity tracking
    popularity_score = models.PositiveIntegerField(
        default=0,
        verbose_name="Popularity Score"
    )
    
    class Meta:
        db_table = 'madi_menu_item'
        verbose_name = "Madi Menu Item"
        verbose_name_plural = "Madi Menu Items"
        ordering = ['display_order', 'created_at']
    
    def get_ingredients_list(self):
        """Return ingredients as a list"""
        if self.ingredients_en:
            return [ingredient.strip() for ingredient in self.ingredients_en.split(',')]
        return []