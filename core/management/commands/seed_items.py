import os

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction


class Command(BaseCommand):
    help = "Seed menus, sections, and items with the real Beresht/Madi menus"

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
        parser.add_argument(
            '--with-inventory',
            action='store_true',
            help='Also seed inventory items for each branch (default: off)',
        )

    def handle(self, *args, **options):
        visuals_dir = options['visuals_dir']

        self.stdout.write(f"Visuals dir: {visuals_dir}")
        self.stdout.write("Items per section flag is ignored; using curated menu data.")

        # Guard against stale schema (branch_id still present) and drop it if needed
        self._ensure_column_dropped('beresht_menu', 'branch_id')
        self._ensure_column_dropped('madi_menu', 'branch_id')

        # Collect image files from visuals/items/ and root visuals/ (optional)
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

        # Collect GIF files from visuals/items/
        gifs = []
        if os.path.isdir(images_dir):
            for fname in os.listdir(images_dir):
                fpath = os.path.join(images_dir, fname)
                if os.path.isfile(fpath) and fname.lower().endswith('.gif'):
                    gifs.append(fpath)
        
        self.stdout.write(self.style.SUCCESS(f"Found {len(gifs)} total gif(s)"))

        # Map brands to their models using explicit imports
        from miyanBeresht.models import BereshtMenu, BereshtMenuSection, BereshtMenuItem
        from miyanMadi.models import MadiMenu, MadiMenuSection, MadiMenuItem
        from miyanGroup.models import Branch, InventoryItem

        brand_configs = [
            {
                'name': 'Beresht',
                'menu_model': BereshtMenu,
                'section_model': BereshtMenuSection,
                'item_model': BereshtMenuItem,
                'branch': Branch.objects.get_or_create(
                    code='beresht', defaults={'name': 'Beresht', 'is_active': True}
                )[0],
            },
            {
                'name': 'Madi',
                'menu_model': MadiMenu,
                'section_model': MadiMenuSection,
                'item_model': MadiMenuItem,
                'branch': Branch.objects.get_or_create(
                    code='madi', defaults={'name': 'Madi', 'is_active': True}
                )[0],
            },
        ]

        main_menu_sections = [
            {
                'title_fa': 'بر پایه اسپرسو - سیاه',
                'title_en': 'Espresso Based - Black',
                'items': [
                    {'name_fa': 'اسپرسو کامرشیال', 'name_en': 'Espresso (Commercial)', 'price_fa': '145'},
                    {'name_fa': 'اسپرسو پرمیوم', 'name_en': 'Espresso (Premium)', 'price_fa': '190'},
                    {'name_fa': 'آمریکانو کامرشیال', 'name_en': 'Americano (Commercial)', 'price_fa': '150'},
                    {'name_fa': 'آمریکانو پرمیوم', 'name_en': 'Americano (Premium)', 'price_fa': '195'},
                    {
                        'name_fa': 'قهوه روز',
                        'name_en': 'Coffee of the Day',
                        'price_fa': '125',
                        'description_fa': '[شارژ رایگان]',
                        'description_en': '[free refill]',
                    },
                ],
            },
            {
                'title_fa': 'بر پایه اسپرسو - سفید',
                'title_en': 'Espresso Based - White',
                'items': [
                    {'name_fa': 'اسپرسو ماکیاتو', 'name_en': 'Espresso Macchiato', 'price_fa': '160'},
                    {'name_fa': 'کورتادو', 'name_en': 'Cortado', 'price_fa': '175'},
                    {'name_fa': 'کاپوچینو', 'name_en': 'Cappuccino', 'price_fa': '185'},
                    {
                        'name_fa': 'لاته',
                        'name_en': 'Latte',
                        'price_fa': '195',
                        'description_fa': '[سرد / گرم]',
                        'description_en': '[iced / hot]',
                    },
                    {
                        'name_fa': 'موکا',
                        'name_en': 'Mocha',
                        'price_fa': '210',
                        'description_fa': '[سرد / گرم]',
                        'description_en': '[iced / hot]',
                    },
                    {'name_fa': 'لاته تیرامیسو', 'name_en': 'Tiramisu Latte', 'price_fa': '280'},
                ],
            },
            {
                'title_fa': 'افزودنی‌ها',
                'title_en': 'Add-ons',
                'items': [
                    {'name_fa': 'عسل', 'name_en': 'Honey', 'price_fa': '+30'},
                    {'name_fa': 'دی کف', 'name_en': 'Decaf', 'price_fa': '+30'},
                    {'name_fa': 'شیر گیاهی', 'name_en': 'Plant-based Milk', 'price_fa': '+75'},
                    {'name_fa': 'سیروپ', 'name_en': 'Syrup', 'price_fa': '+30'},
                    {'name_fa': 'خامه', 'name_en': 'Cream', 'price_fa': '+50'},
                ],
            },
            {
                'title_fa': 'چای و دمنوش',
                'title_en': 'Tea & Infusions',
                'items': [
                    {'name_fa': 'چای سیاه', 'name_en': 'Black Tea', 'price_fa': '110'},
                    {
                        'name_fa': 'ماچا',
                        'name_en': 'Matcha',
                        'price_fa': '210',
                        'description_fa': '[سرد / گرم]',
                        'description_en': '[iced / hot]',
                    },
                    {'name_fa': 'چای سیب و به', 'name_en': 'Apple & Quince Tea', 'price_fa': '135'},
                    {
                        'name_fa': 'چای سبز',
                        'name_en': 'Green Tea',
                        'price_fa': '135',
                        'description_fa': '[بابونه، دارچین، زنجبیل]',
                        'description_en': '[chamomile, cinnamon, ginger]',
                    },
                    {'name_fa': 'دمنوش رز، پنیرک، بابونه، سیب', 'name_en': 'Rose, Mallow, Chamomile, Apple', 'price_fa': '135'},
                    {'name_fa': 'دمنوش دارچین، میخک، زنجبیل', 'name_en': 'Cinnamon, Clove, Ginger', 'price_fa': '135'},
                ],
            },
            {
                'title_fa': 'فراتر',
                'title_en': 'Beyond',
                'items': [
                    {'name_fa': 'هات چاکلت', 'name_en': 'Hot Chocolate', 'price_fa': '270'},
                    {'name_fa': 'ماسالا', 'name_en': 'Masala', 'price_fa': '210'},
                    {
                        'name_fa': 'هات پینات',
                        'name_en': 'Hot Peanut',
                        'price_fa': '175',
                        'description_fa': '[شیر، دارچین، پینات]',
                        'description_en': '[milk, cinnamon, peanut]',
                    },
                    {
                        'name_fa': 'اسپیرولینا',
                        'name_en': 'Spirulina',
                        'price_fa': '210',
                        'description_fa': '[سرد / گرم]',
                        'description_en': '[iced / hot]',
                    },
                    {
                        'name_fa': 'بلوندی',
                        'name_en': 'Blondie',
                        'price_fa': '250',
                        'description_fa': '[شکلات سفید، آلبالو، شیر]',
                        'description_en': '[white chocolate, sour cherry, milk]',
                    },
                ],
            },
            {
                'title_fa': 'نوشیدنی‌های سرد',
                'title_en': 'Cold Drinks',
                'items': [
                    {'name_fa': 'کلد برو', 'name_en': 'Cold Brew', 'price_fa': '275', 'description_fa': 'طعم‌ها: پرتقال کارامل آیریش / آلبالو لیمو'},
                    {'name_fa': 'فیزی آیسد تی', 'name_en': 'Fizzy Iced Tea', 'price_fa': '195', 'description_fa': 'طعم‌ها: انار / انگور سیاه / سودا'},
                    {'name_fa': 'میموسا', 'name_en': 'Mimosa', 'price_fa': '195'},
                    {'name_fa': 'ویشنوکا', 'name_en': 'Vishnuka', 'price_fa': '180'},
                    {
                        'name_fa': 'مرلوت',
                        'name_en': 'Merlot',
                        'price_fa': '195',
                        'description_fa': '[زنجبیل]',
                        'description_en': '[ginger]',
                    },
                    {'name_fa': 'لیموناد', 'name_en': 'Lemonade', 'price_fa': '150'},
                    {'name_fa': 'خاکشیر و آلوئه‌ورا', 'name_en': 'Khakshir & Aloe Vera', 'price_fa': '175'},
                    {
                        'name_fa': 'کلودا',
                        'name_en': 'Cloda',
                        'price_fa': '290',
                        'description_fa': '[سیب دارچین / هلو انبه]',
                        'description_en': '[apple cinnamon / peach mango]',
                    },
                ],
            },
            {
                'title_fa': 'متفرقه',
                'title_en': 'Misc',
                'items': [
                    {'name_fa': 'آبمیوه روز', 'name_en': 'Juice of the Day', 'price_fa': 'از ما بپرسید'},
                ],
            },
        ]

        todays_special_sections = [
            {
                'title_fa': 'کیک و شیرینی',
                'title_en': 'Cakes & Pastries',
                'items': [
                    {'name_fa': 'کروسان بادام', 'name_en': 'Almond Croissant', 'price_fa': '230'},
                    {'name_fa': 'کروسان پاییز', 'name_en': 'Autumn Croissant', 'price_fa': '210'},
                    {'name_fa': 'کروسان شکلاتی', 'name_en': 'Chocolate Croissant', 'price_fa': '180'},
                    {'name_fa': 'رول دارچین', 'name_en': 'Cinnamon Roll', 'price_fa': '170'},
                    {'name_fa': 'پن سوئیسی', 'name_en': 'Pain Suisse', 'price_fa': '175'},
                    {'name_fa': 'تارت فصل', 'name_en': 'Seasonal Tart', 'price_fa': '180'},
                    {'name_fa': 'دماوند', 'name_en': 'Damavand', 'price_fa': '250'},
                    {'name_fa': 'حریره بادام', 'name_en': 'Almond Porridge', 'price_fa': '125'},
                ],
            },
            {
                'title_fa': 'کوکی',
                'title_en': 'Cookies',
                'items': [
                    {'name_fa': 'کوکی دبل چاکلت', 'name_en': 'Double Chocolate Cookie', 'price_fa': '125'},
                    {
                        'name_fa': 'کوکی خرما',
                        'name_en': 'Date Cookie',
                        'price_fa': '125',
                        'description_fa': '[بدون شکر]',
                        'description_en': '[sugar free]',
                    },
                    {
                        'name_fa': 'کوکی هویج و گردو',
                        'name_en': 'Carrot Walnut Cookie',
                        'price_fa': '150',
                        'description_fa': '[بدون شکر]',
                        'description_en': '[sugar free]',
                    },
                ],
            },
            {
                'title_fa': 'میان‌وعده و صبحانه',
                'title_en': 'Snacks & Breakfast',
                'items': [
                    {'name_fa': 'پروتئین بار', 'name_en': 'Protein Bar', 'price_fa': '250'},
                    {'name_fa': 'سرشیر و عسل', 'name_en': 'Cream & Honey', 'price_fa': '245'},
                    {
                        'name_fa': 'اوتمیل',
                        'name_en': 'Oatmeal',
                        'price_fa': '240',
                        'description_fa': '[سوهان عسلی / میوه]',
                        'description_en': '[honey Sohaan / fruit]',
                    },
                ],
            },
            {
                'title_fa': 'تست و نان',
                'title_en': 'Toasts & Bread',
                'items': [
                    {'name_fa': 'تست پنیر شوید', 'name_en': 'Dill Cheese Toast', 'price_fa': '150'},
                    {'name_fa': 'تست پنیر زیره و پسته', 'name_en': 'Cumin Pistachio Cheese Toast', 'price_fa': '280'},
                    {'name_fa': 'تست پینات و عسل', 'name_en': 'Peanut Butter & Honey Toast', 'price_fa': '240'},
                    {
                        'name_fa': 'سیمیت',
                        'name_en': 'Simit',
                        'price_fa': '250',
                        'description_fa': '[پنیر، گوجه، ریحان]',
                        'description_en': '[cheese, tomato, basil]',
                    },
                    {'name_fa': 'کروسان خامه مربا', 'name_en': 'Cream & Jam Croissant', 'price_fa': '150'},
                ],
            },
            {
                'title_fa': 'ساندویچ',
                'title_en': 'Sandwiches',
                'items': [
                    {'name_fa': 'ساندویچ تخم‌مرغ', 'name_en': 'Egg Sandwich', 'price_fa': '245'},
                    {'name_fa': 'چاباتا مرغ و پستو', 'name_en': 'Chicken Pesto Ciabatta', 'price_fa': '375'},
                    {'name_fa': 'چاباتا پولد بیف', 'name_en': 'Pulled Beef Ciabatta', 'price_fa': '435'},
                    {'name_fa': 'چاباتا بیکن', 'name_en': 'Bacon Ciabatta', 'price_fa': '290'},
                ],
            },
            {
                'title_fa': 'متفرقه',
                'title_en': 'Misc Specials',
                'items': [
                    {'name_fa': 'سالاد روز', 'name_en': 'Salad of the Day', 'price_fa': 'از ما بپرسید'},
                ],
            },
        ]

        menus_to_seed = [
            {
                'title_en': "Today's Special",
                'title_fa': 'پخت روز',
                'subtitle_en': '',
                'subtitle_fa': '',
                'menu_type': 'today',
                'sections': todays_special_sections,
            },
            {
                'title_en': 'Main Menu',
                'title_fa': 'منوی نوشیدنی',
                'subtitle_en': '',
                'subtitle_fa': '',
                'menu_type': 'main',
                'sections': main_menu_sections,
            },
        ]

        with transaction.atomic():
            for brand_config in brand_configs:
                brand_name = brand_config['name']
                menu_model = brand_config['menu_model']
                section_model = brand_config['section_model']
                item_model = brand_config['item_model']

                self.stdout.write(f"\n{'='*60}")
                self.stdout.write(f"Brand: {brand_name}")
                self.stdout.write(f"{'='*60}")

                for menu_idx, menu_data in enumerate(menus_to_seed, start=1):
                    menu_defaults = {
                        'title_fa': menu_data['title_fa'],
                        'subtitle_en': menu_data.get('subtitle_en', ''),
                        'subtitle_fa': menu_data.get('subtitle_fa', ''),
                        'is_active': True,
                        'display_order': menu_idx,
                        'menu_type': menu_data.get('menu_type', 'main'),
                    }
                    menu, created = menu_model.objects.get_or_create(
                        title_en=menu_data['title_en'],
                        defaults=menu_defaults,
                    )
                    if not created:
                        for field, value in menu_defaults.items():
                            setattr(menu, field, value)
                        menu.save(update_fields=list(menu_defaults.keys()))

                    self.stdout.write(self.style.SUCCESS(f"✓ Menu: {menu.title_en}"))

                    keep_section_ids = []
                    for section_idx, section_data in enumerate(menu_data['sections'], start=1):
                        section, _ = section_model.objects.get_or_create(
                            menu=menu,
                            title_fa=section_data['title_fa'],
                            title_en=section_data['title_en'],
                            defaults={
                                'description_en': section_data.get('description_en', ''),
                                'description_fa': section_data.get('description_fa', ''),
                                'is_active': True,
                                'display_order': section_idx,
                            },
                        )
                        section.description_en = section_data.get('description_en', '')
                        section.description_fa = section_data.get('description_fa', '')
                        section.is_active = True
                        section.display_order = section_idx
                        section.save(update_fields=['description_en', 'description_fa', 'is_active', 'display_order'])
                        keep_section_ids.append(section.id)

                        keep_item_ids = []
                        for item_idx, item_data in enumerate(section_data.get('items', []), start=1):
                            item, _ = item_model.objects.get_or_create(
                                section=section,
                                name_fa=item_data['name_fa'],
                                defaults={
                                    'name_en': item_data.get('name_en', ''),
                                    'price_fa': item_data.get('price_fa', ''),
                                    'price_en': item_data.get('price_en', item_data.get('price_fa', '')),
                                    'description_fa': item_data.get('description_fa', ''),
                                    'description_en': item_data.get('description_en', ''),
                                    'display_order': item_idx,
                                },
                            )
                            item.name_en = item_data.get('name_en', '')
                            item.price_fa = item_data.get('price_fa', '')
                            item.price_en = item_data.get('price_en', item.price_fa)
                            item.description_fa = item_data.get('description_fa', '')
                            item.description_en = item_data.get('description_en', '')
                            item.display_order = item_idx
                            item.save(update_fields=['name_en', 'price_fa', 'price_en', 'description_fa', 'description_en', 'display_order'])
                            keep_item_ids.append(item.id)

                            # Attach first available image/GIF for a bit of visual variety
                            if images and not item.image:
                                img_path = images[(item_idx - 1) % len(images)]
                                try:
                                    with open(img_path, 'rb') as fp:
                                        item.image.save(os.path.basename(img_path), File(fp), save=True)
                                except Exception as e:
                                    self.stdout.write(self.style.WARNING(f"      Warning: Failed to attach image: {e}"))
                            if gifs and not item.video:
                                gif_path = gifs[(item_idx - 1) % len(gifs)]
                                try:
                                    with open(gif_path, 'rb') as fp:
                                        item.video.save(os.path.basename(gif_path), File(fp), save=True)
                                except Exception as e:
                                    self.stdout.write(self.style.WARNING(f"      Warning: Failed to attach GIF: {e}"))

                        # prune items not in curated list
                        item_model.objects.filter(section=section).exclude(id__in=keep_item_ids).delete()

                    # prune sections not in curated list
                    section_model.objects.filter(menu=menu).exclude(id__in=keep_section_ids).delete()

                if options.get('with_inventory'):
                    inventory_defaults = [
                        {'name': 'Espresso Beans', 'unit': 'kg'},
                        {'name': 'Milk', 'unit': 'L'},
                        {'name': 'Chai Mix', 'unit': 'g'},
                        {'name': 'Pastry Base', 'unit': 'pcs'},
                        {'name': 'Lemonade Syrup', 'unit': 'ml'},
                    ]
                    for inv in inventory_defaults:
                        inv_obj, created = InventoryItem.objects.get_or_create(
                            branch=brand_config['branch'],
                            name=inv['name'],
                            defaults={'unit': inv.get('unit', ''), 'is_active': True},
                        )
                        if created:
                            self.stdout.write(f"  ✓ Inventory item: {inv_obj.name}")

        self.stdout.write(self.style.SUCCESS(f"\n{'='*60}"))
        self.stdout.write(self.style.SUCCESS("✓ Seeding finished with curated menus."))

    # ------------------------------------------------------------------ #
    def _ensure_column_dropped(self, table_name: str, column: str):
        """Drop legacy column if it exists so seeding matches the current models."""
        try:
            with connection.cursor() as cursor:
                cols = connection.introspection.get_table_description(cursor, table_name)
                has_column = any(col.name == column for col in cols)
                if not has_column:
                    return

                self.stdout.write(self.style.WARNING(f"Legacy column `{column}` found on `{table_name}`; dropping it."))
                cursor.execute(f'ALTER TABLE "{table_name}" DROP COLUMN IF EXISTS "{column}";')

                # Re-check to confirm removal
                cols_after = connection.introspection.get_table_description(cursor, table_name)
                if any(col.name == column for col in cols_after):
                    raise CommandError(
                        f"Failed to drop `{column}` from `{table_name}`. "
                        "Please run migrations (e.g. the 0002_remove_*_branch migration) and retry."
                    )
        except Exception:
            # If table is missing (fresh DB) or drop failed unexpectedly, surface a clear error.
            raise CommandError(
                f"Could not verify or drop `{column}` on `{table_name}`. "
                "Ensure migrations are applied and retry seed_items."
            )
