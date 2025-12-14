import secrets
from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from core.models import TimeStampedModel


def generate_telegram_token() -> str:
    """Generate a durable token that staff share with the Telegram bot."""
    return secrets.token_urlsafe(24)


class Branch(TimeStampedModel):
    name = models.CharField(max_length=200, unique=True)
    code = models.SlugField(max_length=64, unique=True, help_text="Short code used by services (e.g., beresht)")
    address = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Branch"
        verbose_name_plural = "Branches"

    def __str__(self) -> str:
        return self.name


class Staff(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff_profile')
    telegram_token = models.CharField(max_length=128, unique=True, default=generate_telegram_token)
    telegram_id = models.CharField(max_length=64, blank=True, null=True)
    language_preference = models.CharField(
        max_length=8,
        choices=[('fa', 'Persian'), ('en', 'Finglish')],
        default='fa',
        help_text="Preferred language for bot replies. 'en' maps to Finglish.",
    )

    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staff"

    def __str__(self) -> str:
        return self.user.get_username()

    @property
    def active_shift(self):
        return self.shifts.filter(ended_at__isnull=True).order_by('-started_at').first()


class StaffBranchAssignment(TimeStampedModel):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='assignments')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='staff_assignments')
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [('staff', 'branch')]
        verbose_name = "Staff Branch Assignment"
        verbose_name_plural = "Staff Branch Assignments"

    def __str__(self) -> str:
        return f"{self.staff} -> {self.branch}"


class StaffShift(TimeStampedModel):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='shifts')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='shifts')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-started_at']
        verbose_name = "Staff Shift"
        verbose_name_plural = "Staff Shifts"

    def __str__(self) -> str:
        status = "active" if not self.ended_at else "ended"
        return f"{self.staff} @ {self.branch} ({status})"

    @property
    def is_active(self) -> bool:
        return self.ended_at is None


class InventoryItem(TimeStampedModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='inventory_items')
    name = models.CharField(max_length=128)
    unit = models.CharField(max_length=32, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [('branch', 'name')]
        ordering = ['branch__name', 'name']
        verbose_name = "Inventory Item"
        verbose_name_plural = "Inventory Items"

    def __str__(self) -> str:
        return f"{self.name} ({self.branch.code})"


class InventoryMeasurement(TimeStampedModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='inventory_measurements')
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='measurements')
    quantity = models.DecimalField(max_digits=12, decimal_places=3, validators=[MinValueValidator(Decimal('0'))])
    recorded_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='measurements')
    measured_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-measured_at']
        verbose_name = "Inventory Measurement"
        verbose_name_plural = "Inventory Measurements"

    def __str__(self) -> str:
        return f"{self.item} @ {self.measured_at:%Y-%m-%d %H:%M}"


class InventoryInput(TimeStampedModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='inventory_inputs')
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='inputs')
    quantity = models.DecimalField(max_digits=12, decimal_places=3, validators=[MinValueValidator(Decimal('0'))])
    note = models.CharField(max_length=255, blank=True)
    recorded_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='inventory_inputs')
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']
        verbose_name = "Inventory Input"
        verbose_name_plural = "Inventory Inputs"

    def __str__(self) -> str:
        return f"{self.item} +{self.quantity}"


class InventoryTransaction(TimeStampedModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='inventory_transactions')
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='transactions')
    note = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='inventory_transactions')

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Inventory Transaction"
        verbose_name_plural = "Inventory Transactions"

    def __str__(self) -> str:
        return f"Txn {self.item} @ {self.branch}"


class MiyanGallery(TimeStampedModel):
    title_en = models.CharField(max_length=200)
    title_fa = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Gallery Item"
        verbose_name_plural = "Gallery"

    def __str__(self):
        return self.title_en
