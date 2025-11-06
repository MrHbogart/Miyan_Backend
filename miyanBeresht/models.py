from django.db import models
from core.models import TimeStampedModel

class MiyanBereshtMenu(TimeStampedModel):
    CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('dessert', 'Dessert'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='lunch')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

    class Meta:
        db_table = 'miyan_beresht_menu'
        verbose_name = "Miyan Beresht Menu Item"
        verbose_name_plural = "Miyan Beresht Menu"

    def __str__(self):
        return f"{self.name} - {self.price}"
