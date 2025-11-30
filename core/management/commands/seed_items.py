import os
import random
from pathlib import Path

from django.apps import apps
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.conf import settings


class Command(BaseCommand):
    help = "Seed menus, sections, and items with images and videos for all menu models"

    def add_arguments(self, parser):
        parser.add_argument(
            '--visuals-dir',
            type=str,
            default='/app/Miyan_Visuals',
            help='Path to visuals directory (default: /app/Miyan_Visuals)'
        )
        parser.add_argument(
            '--items-per-section',
            type=int,
            default=5,
            help='Number of items to create per section (default: 5)'
        )

    def handle(self, *args, **options):
        visuals_dir = options['visuals_dir']
        items_per_section = options['items_per_section']

        self.stdout.write(f"Visuals dir: {visuals_dir}")
        self.stdout.write(f"Items per section: {items_per_section}")

        # Collect image files from visuals/items/
        images_dir = os.path.join(visuals_dir, 'items')
        images = []
        if os.path.isdir(images_dir):
            for fname in os.listdir(images_dir):
                fpath = os.path.join(images_dir, fname)
                if os.path.isfile(fpath) and fname.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    images.append(fpath)
            self.stdout.write(self.style.SUCCESS(f"Found {len(images)} image(s) in {images_dir}"))
        else:
            self.stdout.write(self.style.WARNING(f"Images dir not found: {images_dir}"))

        # Collect video files from visuals/items/
        videos = []
        if os.path.isdir(images_dir):
            for fname in os.listdir(images_dir):
                fpath = os.path.join(images_dir, fname)
                if os.path.isfile(fpath) and fname.lower().endswith(('.mp4', '.webm', '.mov', '.avi')):
                    videos.append(fpath)
            self.stdout.write(self.style.SUCCESS(f"Found {len(videos)} video(s) in {images_dir}"))
        else:
            self.stdout.write(self.style.WARNING(f"Videos dir not found: {images_dir}"))

        # Find menu and section models
        all_models = list(apps.get_models())
        menu_models = [m for m in all_models if m.__name__.endswith('Menu') and not m.__name__.endswith('MenuItem')]
        section_models = {m.__name__: m for m in all_models if m.__name__.endswith('Section')}

        self.stdout.write(f"Menu models: {[m.__name__ for m in menu_models]}")
        self.stdout.write(f"Section models: {list(section_models.keys())}")

        if not menu_models:
            raise CommandError("No menu models found.")

        total_items = 0

        with transaction.atomic():
            for menu_model in menu_models:
                brand_name = menu_model.__module__.split('.')[0]  # e.g., 'miyanBeresht' or 'miyanMadi'
                self.stdout.write(f"\n{'='*60}")
                self.stdout.write(f"Brand: {brand_name}")
                self.stdout.write(f"{'='*60}")

                # Find the section model for this brand
                section_model_name = f"{brand_name.split('miyan')[1].capitalize()}MenuSection"
                section_model = section_models.get(section_model_name)

                if not section_model:
                    self.stdout.write(self.style.ERROR(f"Section model not found for {brand_name}"))
                    continue

                # Find the item model for this brand
                item_model = self._find_item_model(section_model, all_models)
                if not item_model:
                    self.stdout.write(self.style.ERROR(f"Item model not found for {section_model_name}"))
                    continue

                # Create two menus: "Menu" and "Today's Special"
                menus_to_create = [
                    {'title_en': 'Menu', 'title_fa': 'منو', 'subtitle_en': 'Our main menu', 'subtitle_fa': 'منوی اصلی ما'},
                    {'title_en': "Today's Special", 'title_fa': 'ویژه امروز', 'subtitle_en': "Today's special items", 'subtitle_fa': 'اشتهای امروز'},
                ]

                for menu_data in menus_to_create:
                    menu, created = menu_model.objects.get_or_create(
                        title_en=menu_data['title_en'],
                        defaults={
                            'title_fa': menu_data['title_fa'],
                            'subtitle_en': menu_data.get('subtitle_en', ''),
                            'subtitle_fa': menu_data.get('subtitle_fa', ''),
                            'is_active': True,
                            'display_order': 1,
                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"✓ Created menu: {menu}"))
                    else:
                        self.stdout.write(f"  Menu already exists: {menu}")

                    # Create sections for this menu
                    section_types = [
                        {'title_en': 'Appetizers', 'title_fa': 'پیش غذا', 'description_en': 'Start your meal', 'description_fa': 'شروع وعده‌ی خود'},
                        {'title_en': 'Main Courses', 'title_fa': 'غذای اصلی', 'description_en': 'Main dishes', 'description_fa': 'غذاهای اصلی'},
                        {'title_en': 'Desserts', 'title_fa': 'دسر', 'description_en': 'Sweet treats', 'description_fa': 'خوردنی های شیرین'},
                    ]

                    for idx, section_data in enumerate(section_types):
                        section, created = section_model.objects.get_or_create(
                            **{self._get_menu_fk_name(section_model): menu},
                            title_en=section_data['title_en'],
                            defaults={
                                'title_fa': section_data['title_fa'],
                                'description_en': section_data.get('description_en', ''),
                                'description_fa': section_data.get('description_fa', ''),
                                'is_active': True,
                                'display_order': idx + 1,
                            }
                        )

                        if created:
                            self.stdout.write(f"  ✓ Created section: {section}")
                        else:
                            self.stdout.write(f"    Section already exists: {section}")

                        # Create items for this section
                        for item_idx in range(items_per_section):
                            item_name_idx = total_items + item_idx + 1
                            item = item_model()

                            # Set basic fields
                            if hasattr(item, 'name_en'):
                                item.name_en = f"Item {item_name_idx}"
                            if hasattr(item, 'name_fa'):
                                item.name_fa = f"غذای {item_name_idx}"
                            if hasattr(item, 'description_en'):
                                item.description_en = f"Delicious {section_data['title_en'].lower()} item"
                            if hasattr(item, 'description_fa'):
                                item.description_fa = f"یک {section_data['title_fa']} خوشمزه"
                            if hasattr(item, 'price_fa'):
                                item.price_fa = str(random.randint(50000, 250000))
                            if hasattr(item, 'price_en'):
                                item.price_en = item.price_fa

                            # Set section FK
                            self._set_section_fk(item, section, section_model)

                            item.save()

                            # Attach random image
                            if images and hasattr(item, 'image'):
                                img_path = random.choice(images)
                                try:
                                    with open(img_path, 'rb') as fp:
                                        item.image.save(os.path.basename(img_path), File(fp), save=True)
                                except Exception as e:
                                    self.stdout.write(self.style.WARNING(f"      Failed to attach image: {e}"))

                            # Attach random video
                            if videos and hasattr(item, 'video'):
                                video_path = random.choice(videos)
                                try:
                                    with open(video_path, 'rb') as fp:
                                        item.video.save(os.path.basename(video_path), File(fp), save=True)
                                except Exception as e:
                                    self.stdout.write(self.style.WARNING(f"      Failed to attach video: {e}"))

                            self.stdout.write(f"    ✓ Item {item_name_idx}: {item.name_en}")
                            total_items += 1

        self.stdout.write(self.style.SUCCESS(f"\n{'='*60}"))
        self.stdout.write(self.style.SUCCESS(f"✓ Seeding finished. Created {total_items} items."))


    def _get_menu_fk_name(self, section_model):
        """Get the FK field name pointing to the menu model."""
        for field in section_model._meta.fields:
            if hasattr(field, 'related_model') and field.related_model.__name__.endswith('Menu'):
                return field.name
        return None

    def _find_item_model(self, section, all_models):
        """Find concrete item model that FK's to the section."""
        section_class_name = section.__class__.__name__
        # Map section model name to item model name
        # e.g., BereshtMenuSection -> BereshtMenuItem, MadiMenuSection -> MadiMenuItem
        brand_prefix = section_class_name.replace('MenuSection', '')
        expected_item_model_name = f"{brand_prefix}MenuItem"
        
        for model in all_models:
            if model.__name__ == expected_item_model_name:
                # Verify it has FK to the section model
                for field in model._meta.fields:
                    if getattr(field, 'related_model', None) == section.__class__:
                        return model
        
        return None

    def _set_section_fk(self, item, section, section_model):
        """Set the section FK on the item."""
        for field in item._meta.fields:
            if getattr(field, 'related_model', None) == section_model:
                setattr(item, field.name, section)
                return
