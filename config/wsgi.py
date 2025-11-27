import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()


def _auto_collect_static():
    """Ensure collectstatic has run when the app starts in production."""
    if os.getenv('DJANGO_AUTO_COLLECTSTATIC', '1').lower() in {'0', 'false', 'no'}:
        return

    from django.conf import settings

    if settings.DEBUG or getattr(settings, 'RUNNING_TESTS', False):
        return

    static_root = Path(settings.STATIC_ROOT)
    sentinel = static_root / '.static_collected'
    if sentinel.exists():
        return

    static_root.mkdir(parents=True, exist_ok=True)
    lock_path = static_root / '.collectstatic.lock'
    try:
        fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return

    try:
        with os.fdopen(fd, 'w') as lock_file:
            lock_file.write(str(os.getpid()))
        from django.core.management import call_command

        call_command('collectstatic', '--clear', '--noinput', verbosity=0)
        sentinel.write_text('collected')
    finally:
        lock_path.unlink(missing_ok=True)


_auto_collect_static()
