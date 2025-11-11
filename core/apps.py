from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # create default groups if they don't exist yet (safe on migrations)
        try:
            from django.contrib.auth.models import Group
            Group.objects.get_or_create(name='staff')
            Group.objects.get_or_create(name='managers')
            
        except Exception:
            # during initial migrate the auth tables may not be ready; ignore errors
            pass
