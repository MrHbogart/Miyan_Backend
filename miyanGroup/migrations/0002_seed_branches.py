from django.db import migrations


def seed_branches(apps, schema_editor):
    Branch = apps.get_model('miyanGroup', 'Branch')
    defaults = [
        {'name': 'Beresht', 'code': 'beresht', 'is_active': True},
        {'name': 'Madi', 'code': 'madi', 'is_active': True},
    ]
    for entry in defaults:
        Branch.objects.get_or_create(code=entry['code'], defaults=entry)


def reverse_seed(apps, schema_editor):
    Branch = apps.get_model('miyanGroup', 'Branch')
    Branch.objects.filter(code__in=['beresht', 'madi']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('miyanGroup', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_branches, reverse_seed),
    ]
