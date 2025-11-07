from django.conf import settings
from django.db import models


class BaseMenu(models.Model):
    name_fa = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    subtitle_fa = models.CharField(max_length=255, blank=True, null=True)
    subtitle_en = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# class Staff(models.Model):
# 	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff_profile')
# 	role = models.CharField(max_length=100, blank=True)
# 	phone = models.CharField(max_length=30, blank=True)
# 	is_active = models.BooleanField(default=True)

# 	class Meta:
# 		db_table = 'staff'

# 	def __str__(self):
# 		return f"{self.user.get_full_name() or self.user.username} ({self.role})"


# class Ingredient(models.Model):
# 	name = models.CharField(max_length=200, unique=True)
# 	unit = models.CharField(max_length=50, default='unit')
# 	cost_per_unit = models.DecimalField(max_digits=8, decimal_places=3, default=0)
# 	stock_quantity = models.DecimalField(max_digits=10, decimal_places=3, default=0)

# 	class Meta:
# 		db_table = 'ingridients'

# 	def __str__(self):
# 		return self.name


# class Recipe(models.Model):
# 	name = models.CharField(max_length=200)
# 	instructions = models.TextField(blank=True)
# 	ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
# 	prep_time_minutes = models.PositiveIntegerField(null=True, blank=True)
# 	price_estimate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

# 	class Meta:
# 		db_table = 'recipes'

# 	def __str__(self):
# 		return self.name


# class RecipeIngredient(models.Model):
# 	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
# 	ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
# 	quantity = models.DecimalField(max_digits=10, decimal_places=3)
# 	unit = models.CharField(max_length=50, blank=True)

# 	class Meta:
# 		unique_together = ('recipe', 'ingredient')

# 	def __str__(self):
# 		return f"{self.ingredient} x {self.quantity} for {self.recipe}"


# class SellRecord(models.Model):
# 	# Generic relation to any menu item model
# 	content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
# 	object_id = models.PositiveIntegerField()
# 	item = GenericForeignKey('content_type', 'object_id')

# 	item_name = models.CharField(max_length=255)
# 	price = models.DecimalField(max_digits=8, decimal_places=2)
# 	quantity = models.PositiveIntegerField(default=1)
# 	total = models.DecimalField(max_digits=10, decimal_places=2)
# 	sold_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
# 	sold_at = models.DateTimeField(auto_now_add=True)
# 	notes = models.TextField(blank=True)

# 	class Meta:
# 		db_table = 'sellrecords'

# 	def save(self, *args, **kwargs):
# 		# ensure total is consistent
# 		self.total = (self.price or 0) * (self.quantity or 0)
# 		super().save(*args, **kwargs)

# 	def __str__(self):
# 		return f"{self.item_name} x{self.quantity} @ {self.price} on {self.sold_at.isoformat()}"
