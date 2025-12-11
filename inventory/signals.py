from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import StaffProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_staff_profile(sender, instance, created, **kwargs):
    # only create for users that are staff
    if created and getattr(instance, 'is_staff', False):
        StaffProfile.objects.create(user=instance)
