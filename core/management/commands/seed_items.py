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

        # Collect image files from visuals/items/ and root visuals/
        images_dir = os.path.join(visuals_dir, 'items')
        images = []
        
        # Check items subdirectory first
        if os.path.isdir(images_dir):
            for fname in os.listdir(images_dir):
                fpath = os.path.join(images_dir, fname)
                if os.path.isfile(fpath) and fname.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    images.append(fpath)
        
        # Also check root visuals directory for images
        if os.path.isdir(visuals_dir):
            for fname in os.listdir(visuals_dir):
                fpath = os.path.join(visuals_dir, fname)
                if os.path.isfile(fpath) and fname.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    images.append(fpath)
        
        self.stdout.write(self.style.SUCCESS(f"Found {len(images)} total image(s)"))

        # Collect video files from visuals/items/
        videos = []
        if os.path.isdir(images_dir):
            for fname in os.listdir(images_dir):
                fpath = os.path.join(images_dir, fname)
                if os.path.isfile(fpath) and fname.lower().endswith(('.mp4', '.webm', '.mov', '.avi')):
                    videos.append(fpath)
        
        self.stdout.write(self.style.SUCCESS(f"Found {len(videos)} total video(s)"))

        # Map brands to their models using explicit imports
        from miyanBeresht.models import BereshtMenu, BereshtMenuSection, BereshtMenuItem
        from miyanMadi.models import MadiMenu, MadiMenuSection, MadiMenuItem

        brand_configs = [
            {
                'name': 'Beresht',
                'menu_model': BereshtMenu,
                'section_model': BereshtMenuSection,
                'item_model': BereshtMenuItem,
            },
            {
                'name': 'Madi',
                'menu_model': MadiMenu,
                'section_model': MadiMenuSection,
                'item_model': MadiMenuItem,
            },
        ]

        total_items = 0

        with transaction.atomic():
            for brand_config in brand_configs:
                brand_name = brand_config['name']
                menu_model = brand_config['menu_model']
                section_model = brand_config['section_model']
                item_model = brand_config['item_model']

                self.stdout.write(f"\n{'='*60}")
                self.stdout.write(f"Brand: {brand_name}")
                self.stdout.write(f"{'='*60}")

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
                            menu=menu,
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
                            
                            item = item_model(
                                section=section,
                                name_en=f"Item {item_name_idx}",
                                name_fa=f"غذای {item_name_idx}",
                                description_en=f"Delicious {section_data['title_en'].lower()} item",
                                description_fa=f"یک {section_data['title_fa']} خوشمزه",
                                price_fa=str(random.randint(50000, 250000)),
                                display_order=item_idx + 1,
                            )
                            item.price_en = item.price_fa
                            item.save()

                            # Attach random image
                            if images:
                                img_path = random.choice(images)
                                try:
                                    with open(img_path, 'rb') as fp:
                                        item.image.save(os.path.basename(img_path), File(fp), save=True)
                                except Exception as e:
                                    self.stdout.write(self.style.WARNING(f"      Warning: Failed to attach image: {e}"))

                            # Attach random video
                            if videos:
                                video_path = random.choice(videos)
                                try:
                                    with open(video_path, 'rb') as fp:
                                        item.video.save(os.path.basename(video_path), File(fp), save=True)
                                except Exception as e:
                                    self.stdout.write(self.style.WARNING(f"      Warning: Failed to attach video: {e}"))

                            self.stdout.write(f"    ✓ Item {item_name_idx}: {item.name_en}")
                            total_items += 1

        self.stdout.write(self.style.SUCCESS(f"\n{'='*60}"))
        self.stdout.write(self.style.SUCCESS(f"✓ Seeding finished. Created {total_items} items."))

