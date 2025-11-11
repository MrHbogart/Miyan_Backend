from django.db import models

class BaseMenu(models.Model):

    # Main title fields
    title_fa = models.CharField(max_length=255, verbose_name="Title (Persian)")
    title_en = models.CharField(max_length=255, verbose_name="Title (English)")
    
    # Subtitle fields (can be null)
    subtitle_fa = models.CharField(
        max_length=500, 
        blank=True, 
        null=True, 
        verbose_name="Subtitle (Persian)"
    )
    subtitle_en = models.CharField(
        max_length=500, 
        blank=True, 
        null=True, 
        verbose_name="Subtitle (English)"
    )
    
    # Status and ordering
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    class Meta:
        abstract = True
        ordering = ['display_order', 'created_at']


class MenuSection(models.Model):
    """Model for menu sections (like 'Espresso Based', 'Milk Based', etc.)"""
    title_fa = models.CharField(max_length=255, verbose_name="Section Title (Persian)")
    title_en = models.CharField(max_length=255, verbose_name="Section Title (English)")
    
    # Section metadata
    description_fa = models.TextField(blank=True, null=True, verbose_name="Description (Persian)")
    description_en = models.TextField(blank=True, null=True, verbose_name="Description (English)")
    
    # Ordering and status
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ['display_order', 'created_at']
    
    def __str__(self):
        return f"{self.title_en}"


class MenuItem(models.Model):
    """Base model for individual menu items"""
    # Name fields
    name_fa = models.CharField(max_length=255, verbose_name="Item Name (Persian)")
    name_en = models.CharField(max_length=255, verbose_name="Item Name (English)")
    
    # Description fields
    description_fa = models.TextField(blank=True, null=True, verbose_name="Description (Persian)")
    description_en = models.TextField(blank=True, null=True, verbose_name="Description (English)")
    
    # Pricing
    price = models.DecimalField(
        max_digits=32, 
        decimal_places=2, 
        verbose_name="Price",
        help_text="Price in the base currency"
    )
    price_fa = models.CharField(
        max_length=50, 
        verbose_name="Formatted Price (Persian)",
        help_text="Formatted price for display in Persian"
    )
    price_en = models.CharField(
        max_length=50, 
        blank=True,
        verbose_name="Formatted Price (English)",
        help_text="Formatted price for display in English"
    )
    
    # Media
    image = models.ImageField(
        upload_to='menu_items/%Y/%m/%d/', 
        blank=True, 
        null=True,
        verbose_name="Item Image"
    )
    image_url = models.URLField(
        blank=True, 
        null=True,
        verbose_name="External Image URL",
        help_text="Alternative to uploaded image"
    )
    
    # Status and flags
    is_available = models.BooleanField(default=True, verbose_name="Is Available")
    is_todays_special = models.BooleanField(default=False, verbose_name="Today's Special")
    is_featured = models.BooleanField(default=False, verbose_name="Featured Item")
    
    # Dietary and allergen information
    is_vegetarian = models.BooleanField(default=False, verbose_name="Vegetarian")
    is_vegan = models.BooleanField(default=False, verbose_name="Vegan")
    is_gluten_free = models.BooleanField(default=False, verbose_name="Gluten Free")
    contains_allergens = models.CharField(
        max_length=500, 
        blank=True, 
        verbose_name="Contains Allergens",
        help_text="Comma-separated list of allergens"
    )
    
    # Preparation and serving info
    preparation_time = models.PositiveIntegerField(
        blank=True, 
        null=True,
        verbose_name="Preparation Time (minutes)"
    )
    calories = models.PositiveIntegerField(
        blank=True, 
        null=True,
        verbose_name="Calories"
    )
    
    # Ordering
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ['display_order', 'created_at']
    
    def __str__(self):
        return f"{self.name_en} - ${self.price}"
    
    def save(self, *args, **kwargs):
        # Auto-generate formatted prices if not provided
        if not self.price_fa:
            self.price_fa = str(self.price)
        if not self.price_en:
            self.price_en = str(self.price)
        super().save(*args, **kwargs)