from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
import secrets


def generate_bot_token():
    """Generate a unique bot token for staff profiles"""
    return secrets.token_hex(16)


class StaffProfile(models.Model):
    """Developer/IT professional staff profile with bot token for telegram bot access"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bot_token = models.CharField(max_length=64, unique=True, default=generate_bot_token)
    telegram_id = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Staff Profile"
        verbose_name_plural = "Staff Profiles"

    def __str__(self):
        return f"StaffProfile({self.user.username})"


class BaseMenu(models.Model):
    """Base model for menus"""
    
    title_fa = models.CharField(max_length=255, verbose_name="Title (Persian)")
    title_en = models.CharField(max_length=255, verbose_name="Title (English)")
    
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
    
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    show_images = models.BooleanField(
        default=True,
        verbose_name="Show Images",
        help_text="Toggle whether this menu renders item pictures",
    )
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    class Meta:
        abstract = True
        ordering = ['display_order', 'created_at']


class MenuItem(models.Model):
    """Base model for individual menu items"""
    
    name_fa = models.CharField(max_length=255, verbose_name="Item Name (Persian)")
    name_en = models.CharField(max_length=255, verbose_name="Item Name (English)")
    
    description_fa = models.TextField(blank=True, null=True, verbose_name="Description (Persian)")
    description_en = models.TextField(blank=True, null=True, verbose_name="Description (English)")
    
    price_fa = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Formatted Price (Persian)"
    )
    price_en = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Formatted Price (English)"
    )
    
    image = models.ImageField(
        upload_to='menu_items/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Item Image"
    )
    
    video = models.FileField(
        upload_to='menu_items/gifs/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Item Video (GIF)",
        help_text="Animated GIF preview of the item",
        validators=[FileExtensionValidator(['gif'])],
    )
    
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ['display_order', 'created_at']
    
    def __str__(self):
        display_price = self.price_fa or self.price_en or ''
        return f"{self.name_en} {(' - ' + display_price) if display_price else ''}"
