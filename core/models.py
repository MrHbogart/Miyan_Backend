from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class TimeStampedModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class BaseMenu(TimeStampedModel):
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	available = models.BooleanField(default=True)

	class Meta:
		abstract = True

	def __str__(self):
		return f"{self.name} — {self.price}"


class MianBereshtMenu1(BaseMenu):
	class Meta:
		db_table = 'mian_beresht_menu1'
		verbose_name = 'Mian Beresht Menu 1'
		verbose_name_plural = 'Mian Beresht Menu1'


class MianBereshtMenu2(BaseMenu):
	class Meta:
		db_table = 'mian_beresht_menu2'
		verbose_name = 'Mian Beresht Menu 2'
		verbose_name_plural = 'Mian Beresht Menu2'


class MianMadiMenu1(BaseMenu):
	class Meta:
		db_table = 'mian_madi_menu1'
		verbose_name = 'Mian Madi Menu 1'
		verbose_name_plural = 'Mian Madi Menu1'


class MianMadiMenu2(BaseMenu):
	class Meta:
		db_table = 'mian_madi_menu2'
		verbose_name = 'Mian Madi Menu 2'
		verbose_name_plural = 'Mian Madi Menu2'


class Staff(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff_profile')
	role = models.CharField(max_length=100, blank=True)
	phone = models.CharField(max_length=30, blank=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		db_table = 'staff'

	def __str__(self):
		return f"{self.user.get_full_name() or self.user.username} ({self.role})"


class Ingredient(models.Model):
	name = models.CharField(max_length=200, unique=True)
	unit = models.CharField(max_length=50, default='unit')
	cost_per_unit = models.DecimalField(max_digits=8, decimal_places=3, default=0)
	stock_quantity = models.DecimalField(max_digits=10, decimal_places=3, default=0)

	class Meta:
		db_table = 'ingridients'

	def __str__(self):
		return self.name


class Recipe(models.Model):
	name = models.CharField(max_length=200)
	instructions = models.TextField(blank=True)
	ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
	prep_time_minutes = models.PositiveIntegerField(null=True, blank=True)
	price_estimate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

	class Meta:
		db_table = 'recipes'

	def __str__(self):
		return self.name


class RecipeIngredient(models.Model):
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
	ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
	quantity = models.DecimalField(max_digits=10, decimal_places=3)
	unit = models.CharField(max_length=50, blank=True)

	class Meta:
		unique_together = ('recipe', 'ingredient')

	def __str__(self):
		return f"{self.ingredient} x {self.quantity} for {self.recipe}"


class SellRecord(models.Model):
	# Generic relation to any menu item model
	content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
	object_id = models.PositiveIntegerField()
	item = GenericForeignKey('content_type', 'object_id')

	item_name = models.CharField(max_length=255)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)
	total = models.DecimalField(max_digits=10, decimal_places=2)
	sold_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
	sold_at = models.DateTimeField(auto_now_add=True)
	notes = models.TextField(blank=True)

	class Meta:
		db_table = 'sellrecords'

	def save(self, *args, **kwargs):
		# ensure total is consistent
		self.total = (self.price or 0) * (self.quantity or 0)
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.item_name} x{self.quantity} @ {self.price} on {self.sold_at.isoformat()}"
