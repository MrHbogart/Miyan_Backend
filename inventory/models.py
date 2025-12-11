from django.conf import settings
from django.db import models
import secrets


class Branch(models.Model):
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=128)
    unit = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name


class StaffProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bot_token = models.CharField(max_length=64, unique=True, default=lambda: secrets.token_hex(16))
    telegram_id = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"StaffProfile({self.user.username})"


class InventoryRecord(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='records')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='records')
    quantity = models.IntegerField()
    note = models.TextField(blank=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.recorded_at.date()} {self.item.name} x{self.quantity} @ {self.branch.name}"
