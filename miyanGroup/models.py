from django.db import models
from core.models import TimeStampedModel

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
