import os
import random
from pathlib import Path

from django.apps import apps
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
    help = "Seed menu items with random images from a visuals folder"

    def add_arguments(self, parser):
        parser.add_argument(
            '--visuals-dir',
            type=str,
            default='/app/Miyan_Visuals',
            help='Path to visuals directory (default: /app/Miyan_Visuals)'
        )
        parser.add_argument(
            '--items-per-menu',
            type=int,
            default=3,
            help='Number of items to create per menu (default: 3)'
        )

    def handle(self, *args, **options):
        visuals_dir = options['visuals_dir']
        num_items = options['items_per_menu']

        self.stdout.write(f"Visuals dir: {visuals_dir}")
        self.stdout.write(f"Items per menu: {num_items}")

        # collect image files
        images = []
        if os.path.isdir(visuals_dir):
            for fname in os.listdir(visuals_dir):
                fpath = os.path.join(visuals_dir, fname)
                if os.path.isfile(fpath) and fname.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    images.append(fpath)
            self.stdout.write(self.style.SUCCESS(f"Found {len(images)} image(s)"))
        else:
            self.stdout.write(self.style.WARNING(f"Visuals dir not found: {visuals_dir}"))

        # find menu models
        all_models = list(apps.get_models())
        menu_models = [m for m in all_models if m.__name__.endswith('Menu')]
        self.stdout.write(f"Menu models: {[m.__name__ for m in menu_models]}")

        if not menu_models:
            raise CommandError("No menu models found.")

        created_count = 0

        with transaction.atomic():
            for menu_model in menu_models:
                menus = menu_model.objects.all()
                if not menus.exists():
                    self.stdout.write(f"No instances for {menu_model.__name__}")
                    continue

                for menu in menus:
                    self.stdout.write(f"\nProcessing menu: {menu}")

                    # get or create a section
                    section = self._get_or_create_section(menu, menu_model, all_models)
                    if not section:
                        self.stdout.write(self.style.WARNING(f"  Could not find/create section for menu {menu}"))
                        continue

                    # find and create items
                    item_model = self._find_item_model(section, all_models)
                    if not item_model:
                        self.stdout.write(self.style.WARNING(f"  No item model found for section {section}"))
                        continue

                    for i in range(num_items):
                        try:
                            item = item_model()
                            # set fields
                            if hasattr(item, 'name_en'):
                                item.name_en = f"Sample Item {created_count + 1}"
                            if hasattr(item, 'name_fa'):
                                item.name_fa = f"آیتم نمونه {created_count + 1}"
                            if hasattr(item, 'description_en'):
                                item.description_en = "Sample description"
                            if hasattr(item, 'description_fa'):
                                item.description_fa = "توضیح نمونه"
                            if hasattr(item, 'price_fa'):
                                item.price_fa = str(random.randint(50000, 250000))
                            if hasattr(item, 'price_en'):
                                item.price_en = item.price_fa

                            # set section FK
                            self._set_section_fk(item, section)

                            item.save()

                            # attach random image
                            if images and hasattr(item, 'image') and item.image:
                                img_path = random.choice(images)
                                try:
                                    with open(img_path, 'rb') as fp:
                                        item.image.save(os.path.basename(img_path), File(fp), save=True)
                                    self.stdout.write(f"  ✓ Item {created_count + 1} with image: {os.path.basename(img_path)}")
                                except Exception as e:
                                    self.stdout.write(self.style.WARNING(f"  Failed to attach image {img_path}: {e}"))
                            else:
                                self.stdout.write(f"  ✓ Item {created_count + 1} (no image attached)")

                            created_count += 1

                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f"  Failed to create item: {e}"))
                            continue

        self.stdout.write(self.style.SUCCESS(f"\n✓ Seeding finished. Created {created_count} items."))

    def _get_or_create_section(self, menu, menu_model, all_models):
        """Try to get or create a section for the menu."""
        section = None

        # try related_name 'sections'
        if hasattr(menu, 'sections'):
            try:
                if menu.sections.exists():
                    section = menu.sections.first()
                else:
                    section = menu.sections.create(title_fa='بخش نمونه', title_en='Sample Section')
                    self.stdout.write(f"  Created section: {section}")
                return section
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"  Related manager failed: {e}"))

        # fallback: find Section model with FK to menu_model
        for model in all_models:
            if model.__name__.endswith('Section'):
                fk_field = None
                for field in model._meta.fields:
                    if getattr(field, 'related_model', None) == menu_model:
                        fk_field = field
                        break

                if fk_field:
                    kwargs = {fk_field.name: menu}
                    if 'title_en' in [f.name for f in model._meta.fields]:
                        kwargs['title_en'] = 'Sample Section'
                    if 'title_fa' in [f.name for f in model._meta.fields]:
                        kwargs['title_fa'] = 'بخش نمونه'
                    try:
                        section = model.objects.create(**kwargs)
                        self.stdout.write(f"  Created section: {section}")
                        return section
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"  Failed creating fallback section: {e}"))

        return None

    def _find_item_model(self, section, all_models):
        """Find item model that FK's to the section."""
        for model in all_models:
            if model.__name__.endswith('Item'):
                for field in model._meta.fields:
                    if getattr(field, 'related_model', None) == section.__class__:
                        return model
        return None

    def _set_section_fk(self, item, section):
        """Set the section FK on the item."""
        for field in item._meta.fields:
            if getattr(field, 'related_model', None) == section.__class__:
                setattr(item, field.name, section)
                return
