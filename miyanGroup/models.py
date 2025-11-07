from django.db import models

class MiyanGallery(models.Model):
    title_en = models.CharField(max_length=200)
    title_fa = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Gallery Item"
        verbose_name_plural = "Gallery"

    def __str__(self):
        return self.title_en
