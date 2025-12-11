from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'
    verbose_name = 'Inventory'

    def ready(self):
        # import signals to auto-create staff profiles when staff users are created
        try:
            from . import signals  # noqa: F401
        except Exception:
            pass
