#!/usr/bin/env python
"""
Populate Beresht and Madi menu data using the sample images located in
the repository-level Miyan_Pictures directory. This script wipes the
existing menu records and recreates them with consistent demo content
so the frontend can render full menus locally.
"""

import os
import random
import sys
import uuid
from decimal import Decimal
from pathlib import Path

from django.db import transaction
from django.utils.text import slugify
from django.core.files import File

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402

django.setup()

from miyanBeresht.models import (  # noqa: E402
    BereshtMenu,
    BereshtMenuSection,
    BereshtMenuItem,
)
from miyanMadi.models import (  # noqa: E402
    MadiMenu,
    MadiMenuSection,
    MadiMenuItem,
)


PICTURE_DIR = PROJECT_ROOT / "Miyan_Pictures"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
random.seed(42)


def load_image_pool():
    if not PICTURE_DIR.exists():
        raise SystemExit(f"Picture directory not found: {PICTURE_DIR}")
    images = sorted(
        [path for path in PICTURE_DIR.iterdir() if path.suffix.lower() in IMAGE_EXTENSIONS]
    )
    if not images:
        raise SystemExit("No usable images found in Miyan_Pictures")
    return images


IMAGE_POOL = load_image_pool()


def format_price(value: Decimal, locale: str) -> str:
    formatted = f"{int(value):,}"
    return f"{formatted} تومان" if locale == "fa" else f"IRR {formatted}"


def attach_random_image(field_file, base_name: str):
    image_path = random.choice(IMAGE_POOL)
    file_slug = slugify(base_name) or "menu-item"
    filename = f"{file_slug}-{uuid.uuid4().hex[:6]}{image_path.suffix.lower()}"
    with image_path.open("rb") as source:
        field_file.save(filename, File(source), save=True)


def make_price_block(value: Decimal):
    return {
        "price": value,
        "price_fa": format_price(value, "fa"),
        "price_en": format_price(value, "en"),
    }


def madi_menu_payloads():
    return [
        {
            "title_en": "Madi Chef's Noon Table",
            "title_fa": "میز ناهار سرآشپز مادی",
            "subtitle_en": "Limited-run dishes shaped around morning farm deliveries",
            "subtitle_fa": "منویی محدود از مواد اولیه رسیده همان روز",
            "menu_type": "today",
            "service_hours": "12:30 - 15:30",
            "display_order": 1,
            "sections": [
                {
                    "title_en": "Charcoal Starters",
                    "title_fa": "پیش‌غذاهای تنوری",
                    "section_type": "appetizers",
                    "meal_type": "lunch",
                    "description_en": "Vegetables, yogurts, and fire-roasted breads meant for sharing.",
                    "description_fa": "دورهمی کوچکی از سبزیجات دودی و لبنیات مزه‌دار.",
                    "items": [
                        {
                            "name_en": "Smoked Labneh Garden",
                            "name_fa": "لبنه دودی باغچه",
                            "description_en": "Coal-smoked strained yogurt with roasted peppers, charred cucumbers, and seeded lavash chips.",
                            "description_fa": "لبنه دودی با فلفل کبابی، خیار زغالی و لاساش دانه‌دار ترد.",
                            "item_type": "appetizer",
                            "cuisine_type": "persian",
                            "ingredients_en": "labneh, smoked peppers, cucumber, za'atar oil",
                            "ingredients_fa": "لبنه، فلفل دودی، خیار، روغن زعتر",
                            "cooking_method": "Smoked & chilled",
                            "serving_temperature": "Cool",
                            "spice_level": 1,
                            "portion_size": "Shared bowl",
                            "is_vegetarian": True,
                            "is_vegan": False,
                            "contains_allergens": "dairy, sesame",
                            "preparation_time": 10,
                            "calories": 360,
                            "is_todays_special": True,
                            "is_featured": True,
                            "is_chefs_special": True,
                            **make_price_block(Decimal("420000")),
                        },
                        {
                            "name_en": "Saffron Roast Pumpkin",
                            "name_fa": "کدو تنبل زعفرانی",
                            "description_en": "Roasted Hokkaido pumpkin finished with saffron brown butter, candied walnuts, and lime yogurt.",
                            "description_fa": "کدو تنبل کبابی با کره قهوه‌ای زعفرانی، گردوی آبنباتی و ماست لیمویی.",
                            "item_type": "appetizer",
                            "cuisine_type": "fusion",
                            "ingredients_en": "pumpkin, saffron butter, walnut, lime yogurt",
                            "ingredients_fa": "کدو، کره زعفرانی، گردو، ماست لیمویی",
                            "cooking_method": "Oven roasted",
                            "serving_temperature": "Warm",
                            "spice_level": 2,
                            "portion_size": "280g plate",
                            "is_vegetarian": True,
                            "is_vegan": False,
                            "contains_allergens": "dairy, nuts",
                            "preparation_time": 16,
                            "calories": 410,
                            "is_todays_special": True,
                            "is_featured": False,
                            "is_chefs_special": True,
                            **make_price_block(Decimal("480000")),
                        },
                        {
                            "name_en": "Sumac Beef Köfte",
                            "name_fa": "کوفته گوشت سماقی",
                            "description_en": "Griddle-seared beef meatballs with minty broad bean purée, spring onions, and sumac pickles.",
                            "description_fa": "کوفته گوشت روی ساج با پوره باقالی نعنا، پیازچه و ترشی سماق.",
                            "item_type": "appetizer",
                            "cuisine_type": "iranian",
                            "ingredients_en": "beef, broad beans, mint, sumac",
                            "ingredients_fa": "گوشت گوساله، باقالی، نعنا، سماق",
                            "cooking_method": "Griddle seared",
                            "serving_temperature": "Hot",
                            "spice_level": 3,
                            "portion_size": "6 pieces",
                            "is_vegetarian": False,
                            "is_vegan": False,
                            "contains_allergens": "dairy",
                            "preparation_time": 14,
                            "calories": 520,
                            "is_todays_special": True,
                            "is_featured": True,
                            "is_chefs_special": False,
                            **make_price_block(Decimal("510000")),
                        },
                    ],
                },
                {
                    "title_en": "Slow Fire Plates",
                    "title_fa": "غذاهای آتش آرام",
                    "section_type": "main_courses",
                    "meal_type": "dinner",
                    "description_en": "Hearty mains finished over charcoal embers.",
                    "description_fa": "بشقاب‌های سیرکننده که روی ذغال تمام شده‌اند.",
                    "items": [
                        {
                            "name_en": "Pomegranate Glazed Short Rib",
                            "name_fa": "دنده گوساله با لعاب انار",
                            "description_en": "48-hour braised rib lacquered with smoked pomegranate molasses, pea shoots, and toasted pistachio dust.",
                            "description_fa": "دنده گوساله آب‌پز ۴۸ ساعته با رب انار دودی، جوانه نخود و خاک پسته بوداده.",
                            "item_type": "main_course",
                            "cuisine_type": "iranian",
                            "ingredients_en": "beef rib, pomegranate molasses, pistachio",
                            "ingredients_fa": "دنده، رب انار، پسته",
                            "cooking_method": "Slow braised",
                            "serving_temperature": "Hot",
                            "spice_level": 2,
                            "portion_size": "350g bone-in",
                            "is_vegetarian": False,
                            "is_vegan": False,
                            "contains_allergens": "nuts",
                            "is_todays_special": True,
                            "is_featured": True,
                            "is_chefs_special": True,
                            "preparation_time": 20,
                            "calories": 780,
                            **make_price_block(Decimal("890000")),
                        },
                        {
                            "name_en": "Caspian Herb Trout",
                            "name_fa": "قزل‌آلای سبزی کاسپین",
                            "description_en": "Seared trout with sabzi pilaf crumble, pickled grapes, and roasted lemon broth.",
                            "description_fa": "قزل‌آلای سرخ‌شده با کرامبل سبزی‌پلو، انگور ترشی و آب لیموی کبابی.",
                            "item_type": "main_course",
                            "cuisine_type": "mediterranean",
                            "ingredients_en": "trout, herbs, lemon, grapes",
                            "ingredients_fa": "قزل‌آلا، سبزی، لیمو، انگور",
                            "cooking_method": "Pan seared",
                            "serving_temperature": "Hot",
                            "spice_level": 1,
                            "portion_size": "320g fillet",
                            "is_vegetarian": False,
                            "contains_allergens": "fish",
                            "is_todays_special": True,
                            "is_featured": False,
                            "preparation_time": 15,
                            "calories": 540,
                            **make_price_block(Decimal("760000")),
                        },
                        {
                            "name_en": "Charred Cauliflower Tahchin",
                            "name_fa": "ته‌چین گل‌کلم کبابی",
                            "description_en": "Layered saffron rice cake with roasted cauliflower heart, barberries, and smoked yogurt.",
                            "description_fa": "ته‌چین زعفرانی با قلب گل‌کلم برشته، زرشک و ماست دودی.",
                            "item_type": "main_course",
                            "cuisine_type": "persian",
                            "ingredients_en": "saffron rice, cauliflower, yogurt",
                            "ingredients_fa": "برنج زعفرانی، گل‌کلم، ماست",
                            "cooking_method": "Baked & charred",
                            "serving_temperature": "Hot",
                            "spice_level": 1,
                            "portion_size": "Slice for two",
                            "is_vegetarian": True,
                            "is_todays_special": False,
                            "is_featured": True,
                            "contains_allergens": "dairy",
                            "preparation_time": 18,
                            "calories": 690,
                            **make_price_block(Decimal("650000")),
                        },
                    ],
                },
                {
                    "title_en": "Glow Desserts",
                    "title_fa": "دسرهای درخشان",
                    "section_type": "desserts",
                    "meal_type": "any",
                    "description_en": "Light, floral, and chilled finishes to lunch.",
                    "description_fa": "پایان لطیف و گلی برای ناهار.",
                    "items": [
                        {
                            "name_en": "Saffron Pistachio Parfait",
                            "name_fa": "پارفی زعفران و پسته",
                            "description_en": "Frozen parfait with roasted pistachios, tonic-soaked figs, and brittle shards.",
                            "description_fa": "پارفی منجمد با پسته برشته، انجیر در تونیک و تافی ترد.",
                            "item_type": "dessert",
                            "cuisine_type": "persian",
                            "ingredients_en": "pistachio, saffron, figs",
                            "ingredients_fa": "پسته، زعفران، انجیر",
                            "cooking_method": "Frozen",
                            "serving_temperature": "Cold",
                            "spice_level": 0,
                            "portion_size": "Individual glass",
                            "is_vegetarian": True,
                            "is_gluten_free": True,
                            "is_todays_special": True,
                            "preparation_time": 5,
                            "calories": 420,
                            **make_price_block(Decimal("360000")),
                        },
                        {
                            "name_en": "Lavender Rice Pudding",
                            "name_fa": "شیر برنج لاوندر",
                            "description_en": "Creamy rice pudding steeped with lavender smoke and candied quince.",
                            "description_fa": "شیر برنج کرمی با دود لاوندر و به قندی.",
                            "item_type": "dessert",
                            "cuisine_type": "persian",
                            "ingredients_en": "rice, milk, lavender, quince",
                            "ingredients_fa": "برنج، شیر، لاوندر، به",
                            "cooking_method": "Slow simmered",
                            "serving_temperature": "Warm",
                            "spice_level": 0,
                            "portion_size": "Stone bowl",
                            "is_vegetarian": True,
                            "contains_allergens": "dairy",
                            "is_todays_special": False,
                            "preparation_time": 8,
                            "calories": 380,
                            **make_price_block(Decimal("330000")),
                        },
                        {
                            "name_en": "Cardamom Chocolate Pebbles",
                            "name_fa": "سنگریزه شکلاتی هل",
                            "description_en": "Crunchy chocolate mousse rocks with cardamom dust, cocoa nib brittle, and sea salt caramel.",
                            "description_fa": "سنگریزه موس شکلاتی با هل ساییده، بریتل کاکائو و کارامل نمکی.",
                            "item_type": "dessert",
                            "cuisine_type": "fusion",
                            "ingredients_en": "dark chocolate, cardamom, caramel",
                            "ingredients_fa": "شکلات تلخ، هل، کارامل",
                            "cooking_method": "Chilled mousse",
                            "serving_temperature": "Cold",
                            "spice_level": 0,
                            "portion_size": "Shared plate",
                            "is_vegetarian": True,
                            "contains_allergens": "dairy",
                            "is_todays_special": False,
                            "preparation_time": 7,
                            "calories": 460,
                            **make_price_block(Decimal("390000")),
                        },
                    ],
                },
                {
                    "title_en": "Charred Garden Sides",
                    "title_fa": "دورچین‌های باغ شعله",
                    "section_type": "sides",
                    "meal_type": "lunch",
                    "description_en": "Seasonal vegetables and grains finished over open fire.",
                    "description_fa": "سبزیجات و غلات فصل که روی آتش باز کامل شده‌اند.",
                    "items": [
                        {
                            "name_en": "Coal Roasted Baby Carrots",
                            "name_fa": "هویج مینی زغالی",
                            "description_en": "Ember-roasted baby carrots glazed with sour orange, herb tahini, and dukkah crunch.",
                            "description_fa": "هویج‌های مینی برشته با لیمو شیرین، ارده سبزی و کراس دوکا.",
                            "item_type": "side_dish",
                            "cuisine_type": "fusion",
                            "ingredients_en": "baby carrot, sour orange, tahini, dukkah",
                            "ingredients_fa": "هویج مینی، نارنج، ارده، دوکا",
                            "cooking_method": "Ember roasted",
                            "serving_temperature": "Hot",
                            "spice_level": 2,
                            "portion_size": "Sharing plate",
                            "is_vegetarian": True,
                            "is_vegan": True,
                            "contains_allergens": "sesame, nuts",
                            "preparation_time": 11,
                            "calories": 260,
                            "is_todays_special": True,
                            "is_featured": True,
                            **make_price_block(Decimal("360000")),
                        },
                        {
                            "name_en": "Black Lime Ash Mash",
                            "name_fa": "پوره آش لیموعمانی",
                            "description_en": "Rustic vegetable mash infused with smoked black lime oil, pickled shallots, and toasted lentils.",
                            "description_fa": "پوره سبزیجات با روغن لیموعمانی دودی، موسیر ترشی و عدس برشته.",
                            "item_type": "side_dish",
                            "cuisine_type": "iranian",
                            "ingredients_en": "root vegetables, black lime, lentils",
                            "ingredients_fa": "سبزیجات ریشه‌ای، لیموعمانی، عدس",
                            "cooking_method": "Smoked mash",
                            "serving_temperature": "Warm",
                            "spice_level": 1,
                            "portion_size": "Clay bowl",
                            "is_vegetarian": True,
                            "is_vegan": False,
                            "contains_allergens": "dairy",
                            "preparation_time": 9,
                            "calories": 310,
                            "is_todays_special": True,
                            "is_featured": False,
                            **make_price_block(Decimal("330000")),
                        },
                        {
                            "name_en": "Garden Herb Rice Chips",
                            "name_fa": "چیپس برنج سبزی",
                            "description_en": "Crispy tahdig shards dusted with garden herbs, smoked salt, and fenugreek dip.",
                            "description_fa": "تکه‌های ته‌دیگ ترد با سبزی باغچه، نمک دودی و دیپ شنبلیله.",
                            "item_type": "side_dish",
                            "cuisine_type": "iranian",
                            "ingredients_en": "rice, herbs, fenugreek yogurt",
                            "ingredients_fa": "برنج، سبزیجات، ماست شنبلیله",
                            "cooking_method": "Pan fried",
                            "serving_temperature": "Warm",
                            "spice_level": 0,
                            "portion_size": "Snack bowl",
                            "is_vegetarian": True,
                            "is_todays_special": True,
                            "contains_allergens": "dairy",
                            "preparation_time": 6,
                            "calories": 280,
                            **make_price_block(Decimal("290000")),
                        },
                    ],
                },
            ],
        },
        {
            "title_en": "Madi All-Day Gallery",
            "title_fa": "گالری تمام‌روزه مادی",
            "subtitle_en": "Breakfast rituals, clay-pot classics, and sunset sweets.",
            "subtitle_fa": "از صبحانه تا دسرهای غروب.",
            "menu_type": "main",
            "service_hours": "08:00 - 23:00",
            "display_order": 2,
            "sections": [
                {
                    "title_en": "Breakfast Atelier",
                    "title_fa": "کارگاه صبحانه",
                    "section_type": "breakfast",
                    "meal_type": "breakfast",
                    "description_en": "Plates designed for slow, layered breakfasts.",
                    "description_fa": "صبحانه‌هایی برای شروع آرام روز.",
                    "items": [
                        {
                            "name_en": "Barberry Pistachio French Toast",
                            "name_fa": "فرنچ‌تست زرشک و پسته",
                            "description_en": "Custard-soaked brioche with saffron syrup, toasted pistachio crumble, and barberry compote.",
                            "description_fa": "بریوش کاراملی با شربت زعفران، کرامبل پسته و کمپوت زرشک.",
                            "item_type": "breakfast",
                            "cuisine_type": "fusion",
                            "ingredients_en": "brioche, saffron syrup, pistachio, barberry",
                            "ingredients_fa": "بریوش، شربت زعفران، پسته، زرشک",
                            "cooking_method": "Pan fried",
                            "serving_temperature": "Warm",
                            "spice_level": 0,
                            "portion_size": "2 slices",
                            "is_vegetarian": True,
                            "is_featured": True,
                            "contains_allergens": "gluten, dairy, eggs, nuts",
                            "preparation_time": 12,
                            "calories": 640,
                            **make_price_block(Decimal("520000")),
                        },
                        {
                            "name_en": "Savory Herb Omelette",
                            "name_fa": "املت سبزیجات معطر",
                            "description_en": "Three-egg omelette with sabzi khordan, smoked feta, and tomato jam.",
                            "description_fa": "املت سه تخم‌مرغ با سبزی خوردن، فتا دودی و مربای گوجه.",
                            "item_type": "breakfast",
                            "cuisine_type": "persian",
                            "ingredients_en": "egg, feta, herbs, tomato",
                            "ingredients_fa": "تخم‌مرغ، فتا، سبزی، گوجه",
                            "cooking_method": "Skillet",
                            "serving_temperature": "Hot",
                            "spice_level": 1,
                            "portion_size": "Skillet for one",
                            "is_vegetarian": True,
                            "contains_allergens": "eggs, dairy",
                            "preparation_time": 9,
                            "calories": 510,
                            **make_price_block(Decimal("430000")),
                        },
                        {
                            "name_en": "Sesame Tahini Porridge",
                            "name_fa": "فرنی کنجد و ارده",
                            "description_en": "Steel-cut oats cooked with tahini milk, pistachio butter, and honeyed figs.",
                            "description_fa": "گرده جو دوسر با شیر ارده، کره پسته و انجیر عسلی.",
                            "item_type": "breakfast",
                            "cuisine_type": "mediterranean",
                            "ingredients_en": "oats, tahini milk, figs",
                            "ingredients_fa": "جو دوسر، شیر ارده، انجیر",
                            "cooking_method": "Slow simmered",
                            "serving_temperature": "Warm",
                            "spice_level": 0,
                            "portion_size": "Clay pot",
                            "is_vegetarian": True,
                            "is_vegan": False,
                            "contains_allergens": "sesame, nuts",
                            "preparation_time": 8,
                            "calories": 420,
                            **make_price_block(Decimal("390000")),
                        },
                    ],
                },
                {
                    "title_en": "Clay Pot Classics",
                    "title_fa": "کلاسیک‌های دیگ سفالی",
                    "section_type": "main_courses",
                    "meal_type": "dinner",
                    "description_en": "Comfort dishes with deeply reduced broths and smoke.",
                    "description_fa": "غذاهای دودی و مرمری با لعاب‌های غلیظ.",
                    "items": [
                        {
                            "name_en": "Heritage Lamb Shank",
                            "name_fa": "ماهیچه بره اصیل",
                            "description_en": "Clay-braised lamb shank with dried lime jus, smoked shallots, and dill rice mash.",
                            "description_fa": "ماهیچه بره در دیگ با عصاره لیمو عمانی، موسیر دودی و پوره شویدپلو.",
                            "item_type": "main_course",
                            "cuisine_type": "iranian",
                            "ingredients_en": "lamb, dried lime, dill rice",
                            "ingredients_fa": "ماهیچه، لیمو عمانی، شویدپلو",
                            "cooking_method": "Clay pot braised",
                            "serving_temperature": "Hot",
                            "spice_level": 3,
                            "portion_size": "450g shank",
                            "is_todays_special": False,
                            "is_featured": True,
                            "is_chefs_special": False,
                            "contains_allergens": "",
                            "preparation_time": 22,
                            "calories": 820,
                            **make_price_block(Decimal("910000")),
                        },
                        {
                            "name_en": "Sour Cherry Duck Pilaf",
                            "name_fa": "پلو آلبالو با اردک",
                            "description_en": "Roasted duck breast, sour cherry pilaf, toasted almonds, and pickled flowers.",
                            "description_fa": "سینه اردک برشته با پلو آلبالو، بادام بوداده و گل ترشی.",
                            "item_type": "main_course",
                            "cuisine_type": "persian",
                            "ingredients_en": "duck, sour cherry, almond",
                            "ingredients_fa": "اردک، آلبالو، بادام",
                            "cooking_method": "Roasted",
                            "serving_temperature": "Hot",
                            "spice_level": 2,
                            "portion_size": "360g plate",
                            "is_todays_special": False,
                            "is_featured": True,
                            "contains_allergens": "nuts",
                            "preparation_time": 18,
                            "calories": 710,
                            **make_price_block(Decimal("840000")),
                        },
                        {
                            "name_en": "Garden Herb Ash Reshteh",
                            "name_fa": "آش رشته سبزی باغ",
                            "description_en": "Rich vegetable and noodle stew with herb oil drizzle and crispy chickpeas.",
                            "description_fa": "آش رشته پرملات با روغن سبزی و نخودچی ترد.",
                            "item_type": "main_course",
                            "cuisine_type": "iranian",
                            "ingredients_en": "herbs, beans, noodles",
                            "ingredients_fa": "سبزی، حبوبات، رشته",
                            "cooking_method": "Stewed",
                            "serving_temperature": "Hot",
                            "spice_level": 1,
                            "portion_size": "Copper bowl",
                            "is_vegetarian": True,
                            "is_todays_special": False,
                            "contains_allergens": "gluten",
                            "preparation_time": 14,
                            "calories": 560,
                            **make_price_block(Decimal("420000")),
                        },
                    ],
                },
                {
                    "title_en": "Teahouse Desserts",
                    "title_fa": "دسرهای چایخانه",
                    "section_type": "desserts",
                    "meal_type": "any",
                    "description_en": "Treats paired with Madi's samovar service.",
                    "description_fa": "دسترسی‌های هماهنگ با سرویس سماور مادی.",
                    "items": [
                        {
                            "name_en": "Caramelized Fig Baklava",
                            "name_fa": "باقلوای انجیر کاراملی",
                            "description_en": "Rolled baklava with fig caramel, pistachio praline, and rose dust.",
                            "description_fa": "باقلوا رولتی با کارامل انجیر، پرالین پسته و غبار گل‌محمدی.",
                            "item_type": "dessert",
                            "cuisine_type": "persian",
                            "ingredients_en": "fig, pistachio, phyllo, rose",
                            "ingredients_fa": "انجیر، پسته، خمیر فیلو، گل محمدی",
                            "cooking_method": "Baked",
                            "serving_temperature": "Warm",
                            "spice_level": 0,
                            "portion_size": "3 rolls",
                            "is_vegetarian": True,
                            "contains_allergens": "nuts, gluten",
                            "preparation_time": 6,
                            "calories": 480,
                            **make_price_block(Decimal("360000")),
                        },
                        {
                            "name_en": "Orange Blossom Cheesecake",
                            "name_fa": "چیزکیک بهار نارنج",
                            "description_en": "Baked cheesecake scented with orange blossom, saffron honey, and almond soil.",
                            "description_fa": "چیزکیک پخته با رایحه بهار نارنج، عسل زعفرانی و خاک بادام.",
                            "item_type": "dessert",
                            "cuisine_type": "fusion",
                            "ingredients_en": "cream cheese, orange blossom, almond",
                            "ingredients_fa": "پنیر خامه‌ای، بهار نارنج، بادام",
                            "cooking_method": "Baked",
                            "serving_temperature": "Cool",
                            "spice_level": 0,
                            "portion_size": "Slice",
                            "is_vegetarian": True,
                            "contains_allergens": "dairy, eggs, nuts",
                            "preparation_time": 5,
                            "calories": 520,
                            **make_price_block(Decimal("380000")),
                        },
                        {
                            "name_en": "Sour Cherry Sorbet Float",
                            "name_fa": "سوربه آلبالو با چای سرد",
                            "description_en": "Sour cherry sorbet served in iced black tea with candied orange peel.",
                            "description_fa": "سوربه آلبالو در چای سیاه یخ‌زده با پوست پرتقال قندی.",
                            "item_type": "dessert",
                            "cuisine_type": "international",
                            "ingredients_en": "sour cherry, tea, orange peel",
                            "ingredients_fa": "آلبالو، چای، پوست پرتقال",
                            "cooking_method": "Frozen",
                            "serving_temperature": "Cold",
                            "spice_level": 0,
                            "portion_size": "Glass",
                            "is_vegetarian": True,
                            "is_vegan": True,
                            "preparation_time": 4,
                            "calories": 190,
                            **make_price_block(Decimal("310000")),
                        },
                    ],
                },
                {
                    "title_en": "Sunset Mezze Spread",
                    "title_fa": "پیشخوان مزه غروب",
                    "section_type": "appetizers",
                    "meal_type": "dinner",
                    "description_en": "Shared plates that bridge afternoon tea and dinner service.",
                    "description_fa": "بشقاب‌های مشترک میان عصرانه و شام.",
                    "items": [
                        {
                            "name_en": "Charred Eggplant Rain",
                            "name_fa": "باران بادمجان کبابی",
                            "description_en": "Flame-licked eggplant ribbons with whey espuma, dried lime crumbs, and herbs.",
                            "description_fa": "نواره‌های بادمجان آتشی با فوم کشک، خاک لیمو و سبزی تازه.",
                            "item_type": "appetizer",
                            "cuisine_type": "iranian",
                            "ingredients_en": "eggplant, whey, dried lime",
                            "ingredients_fa": "بادمجان، کشک، لیموعمانی",
                            "cooking_method": "Charred",
                            "serving_temperature": "Warm",
                            "spice_level": 2,
                            "portion_size": "Sharing platter",
                            "is_vegetarian": True,
                            "is_todays_special": True,
                            "contains_allergens": "dairy",
                            "preparation_time": 10,
                            "calories": 420,
                            **make_price_block(Decimal("480000")),
                        },
                        {
                            "name_en": "Smoked Yogurt Dolmeh",
                            "name_fa": "دلمه ماست دودی",
                            "description_en": "Grape leaves filled with smoked yogurt rice, pistachio crumble, and mint oil.",
                            "description_fa": "برگ مو با برنج ماست دودی، کرامبل پسته و روغن نعنا.",
                            "item_type": "appetizer",
                            "cuisine_type": "persian",
                            "ingredients_en": "grape leaves, yogurt rice, pistachio",
                            "ingredients_fa": "برگ مو، برنج ماستی، پسته",
                            "cooking_method": "Steamed",
                            "serving_temperature": "Warm",
                            "spice_level": 1,
                            "portion_size": "5 pieces",
                            "is_vegetarian": True,
                            "is_todays_special": True,
                            "contains_allergens": "dairy, nuts",
                            "preparation_time": 12,
                            "calories": 360,
                            **make_price_block(Decimal("460000")),
                        },
                        {
                            "name_en": "Smoked Lamb Belly Skewers",
                            "name_fa": "سیخچه دنده بره دودی",
                            "description_en": "Quick-seared lamb belly skewers with pomegranate drizzle and crispy herbs.",
                            "description_fa": "سیخچه‌های شکم بره با سس انار و سبزی ترد.",
                            "item_type": "appetizer",
                            "cuisine_type": "iranian",
                            "ingredients_en": "lamb belly, pomegranate, herbs",
                            "ingredients_fa": "دنده بره، انار، سبزی",
                            "cooking_method": "Skewered & seared",
                            "serving_temperature": "Hot",
                            "spice_level": 3,
                            "portion_size": "3 skewers",
                            "is_todays_special": False,
                            "contains_allergens": "",
                            "preparation_time": 9,
                            "calories": 540,
                            **make_price_block(Decimal("520000")),
                        },
                    ],
                },
            ],
        },
    ]


def beresht_menu_payloads():
    return [
        {
            "title_en": "Beresht Brew Lab Today",
            "title_fa": "لابراتوار امروز برشت",
            "subtitle_en": "Limited pours, garden sandwiches, and tonic pairings.",
            "subtitle_fa": "اسپرسوهای محدود و ساندویچ‌های باغچه‌ای.",
            "menu_type": "today",
            "display_order": 1,
            "sections": [
                {
                    "title_en": "Espresso Rituals",
                    "title_fa": "مناسک اسپرسو",
                    "section_type": "beverages",
                    "description_en": "Microlot espressos dialed in for the day.",
                    "description_fa": "اسپرسوهای میکرولات تنظیم شده همان روز.",
                    "items": [
                        {
                            "name_en": "Juniper Tonic Espresso",
                            "name_fa": "اسپرسو تونیک سرو",
                            "description_en": "Double shot over juniper tonic, dehydrated citrus, and rosemary smoke.",
                            "description_fa": "دبل شات روی تونیک سرو با مرکبات خشک و دود رزماری.",
                            "item_type": "espresso",
                            "available_sizes": "Double",
                            "spice_level": 0,
                            "ingredients_en": "espresso, tonic, juniper, rosemary",
                            "ingredients_fa": "اسپرسو، تونیک، سرو، رزماری",
                            "is_todays_special": True,
                            "is_featured": True,
                            "is_vegetarian": True,
                            "is_vegan": True,
                            **make_price_block(Decimal("210000")),
                        },
                        {
                            "name_en": "Cardamom Cortado",
                            "name_fa": "کرتادو هل",
                            "description_en": "Single-origin espresso pulled short, textured milk, cardamom mist.",
                            "description_fa": "اسپرسوی تک‌مزرعه با شیر فومی و بخار هل.",
                            "item_type": "espresso",
                            "available_sizes": "Single,Double",
                            "spice_level": 1,
                            "ingredients_en": "espresso, milk, cardamom",
                            "ingredients_fa": "اسپرسو، شیر، هل",
                            "is_todays_special": True,
                            "is_featured": False,
                            "contains_allergens": "dairy",
                            **make_price_block(Decimal("180000")),
                        },
                        {
                            "name_en": "Honeycomb Flat White",
                            "name_fa": "فلت وایت شهدی",
                            "description_en": "Velvety flat white finished with raw honeycomb and cacao nibs.",
                            "description_fa": "فلت وایت مخملی با موم عسل تازه و نیب کاکائو.",
                            "item_type": "milk",
                            "available_sizes": "Double",
                            "spice_level": 0,
                            "contains_allergens": "dairy",
                            "is_todays_special": False,
                            "is_featured": True,
                            **make_price_block(Decimal("195000")),
                        },
                    ],
                },
                {
                    "title_en": "Garden Sandwiches",
                    "title_fa": "ساندویچ‌های باغچه‌ای",
                    "section_type": "food",
                    "description_en": "Warm sandwiches layered with slow-roasted vegetables and herb chutneys.",
                    "description_fa": "ساندویچ‌های گرم با سبزیجات برشته و چاتنی‌های معطر.",
                    "items": [
                        {
                            "name_en": "Roasted Beet Feta Melt",
                            "name_fa": "ملیت چغندر و فتا",
                            "description_en": "Charred beet slices, whipped feta, almond pesto, and rye.",
                            "description_fa": "برش‌های چغندر برشته، فتا زده شده، پستو بادام و نان چاودار.",
                            "item_type": "food",
                            "available_sizes": "",
                            "spice_level": 1,
                            "ingredients_en": "beet, feta, almond, rye",
                            "ingredients_fa": "چغندر، فتا، بادام، چاودار",
                            "is_vegetarian": True,
                            "contains_allergens": "gluten, nuts, dairy",
                            "preparation_time": 8,
                            **make_price_block(Decimal("320000")),
                        },
                        {
                            "name_en": "Citrus Chicken Brioche",
                            "name_fa": "بریوش مرغ مرکباتی",
                            "description_en": "Poached chicken, preserved lemon aioli, pickled fennel, and basil oil.",
                            "description_fa": "مرغ آب‌پز، ایولی لیمو شور، فنل ترشی و روغن ریحان.",
                            "item_type": "food",
                            "spice_level": 2,
                            "ingredients_en": "chicken, lemon, fennel, brioche",
                            "ingredients_fa": "مرغ، لیمو، فنل، بریوش",
                            "contains_allergens": "eggs, gluten",
                            "preparation_time": 9,
                            **make_price_block(Decimal("360000")),
                        },
                        {
                            "name_en": "Smoked Mushroom Toastie",
                            "name_fa": "توستی قارچ دودی",
                            "description_en": "Smoked oyster mushrooms, caramelized onions, and truffle labneh on sourdough.",
                            "description_fa": "قارچ صدفی دودی، پیاز کاراملی و لبنه ترافل روی خمیرترش.",
                            "item_type": "food",
                            "spice_level": 1,
                            "is_vegetarian": True,
                            "contains_allergens": "gluten, dairy",
                            "preparation_time": 7,
                            **make_price_block(Decimal("340000")),
                        },
                    ],
                },
                {
                    "title_en": "Iced Tonic Lab",
                    "title_fa": "لابراتوار تونیک یخ",
                    "section_type": "specials",
                    "description_en": "Sparkling coffee tonics layered with botanicals.",
                    "description_fa": "تونیک‌های قهوه با لایه‌های گیاهی.",
                    "items": [
                        {
                            "name_en": "Seville Cold Brew Fizz",
                            "name_fa": "فیز قهوه سویا",
                            "description_en": "Slow-drip cold brew, seville orange tonic, saffron mist.",
                            "description_fa": "کولدبرو قطره‌ای، تونیک پرتقال سویا و میست زعفران.",
                            "item_type": "specialty",
                            "available_sizes": "Single",
                            "spice_level": 0,
                            "is_todays_special": True,
                            "is_featured": True,
                            **make_price_block(Decimal("230000")),
                        },
                        {
                            "name_en": "Grapefruit Cascara Spritz",
                            "name_fa": "اسپریتز کاسکارا گریپ‌فروت",
                            "description_en": "Cascara reduction, grapefruit tonic, and lemongrass cloud.",
                            "description_fa": "غلظت کاسکارا، تونیک گریپ‌فروت و کف لمون‌گراس.",
                            "item_type": "specialty",
                            "spice_level": 0,
                            "is_vegan": True,
                            "is_todays_special": False,
                            **make_price_block(Decimal("220000")),
                        },
                        {
                            "name_en": "Pink Pepper Nitro",
                            "name_fa": "نیترو فلفل صورتی",
                            "description_en": "Nitro cold brew, pink peppercorn syrup, rose petal dust.",
                            "description_fa": "کولدبرو نیترو، شربت فلفل صورتی و غبار گل سرخ.",
                            "item_type": "specialty",
                            "spice_level": 1,
                            "is_todays_special": True,
                            **make_price_block(Decimal("240000")),
                        },
                    ],
                },
                {
                    "title_en": "Botanical Pastries",
                    "title_fa": "شیرینی‌های گیاهی",
                    "section_type": "desserts",
                    "description_en": "Limited pastries infused with citrus oils, herbs, and botanicals.",
                    "description_fa": "شیرینی‌های محدود با روغن مرکبات و گیاهان معطر.",
                    "items": [
                        {
                            "name_en": "Verbena Pistachio Kouign",
                            "name_fa": "کوئین وربنا و پسته",
                            "description_en": "Laminate dough caramelized with verbena syrup and pistachio praline cream.",
                            "description_fa": "خمیر لایه‌ای کاراملی با شربت وربنا و کرم پرالین پسته.",
                            "item_type": "dessert",
                            "spice_level": 0,
                            "ingredients_en": "butter dough, verbena, pistachio",
                            "ingredients_fa": "خمیر کره‌ای، وربنا، پسته",
                            "is_vegetarian": True,
                            "contains_allergens": "dairy, gluten, nuts",
                            "is_todays_special": True,
                            **make_price_block(Decimal("310000")),
                        },
                        {
                            "name_en": "Lavender Citrus Financier",
                            "name_fa": "فینانسیه لاوندر و مرکبات",
                            "description_en": "Mini almond cakes soaked with lavender honey and grapefruit zest.",
                            "description_fa": "کیک بادام کوچک با عسل لاوندر و پوست گریپ‌فروت.",
                            "item_type": "dessert",
                            "spice_level": 0,
                            "is_vegetarian": True,
                            "contains_allergens": "nuts, eggs, dairy",
                            "is_todays_special": True,
                            **make_price_block(Decimal("260000")),
                        },
                        {
                            "name_en": "Rosemary Cloud Choux",
                            "name_fa": "شو خامه‌ای ابری رزماری",
                            "description_en": "Choux pastry with rosemary cream, pink pepper caramel, and cacao dust.",
                            "description_fa": "شو خامه‌ای با کرم رزماری، کارامل فلفل صورتی و پودر کاکائو.",
                            "item_type": "dessert",
                            "spice_level": 0,
                            "is_vegetarian": True,
                            "contains_allergens": "gluten, dairy, eggs",
                            "is_todays_special": False,
                            **make_price_block(Decimal("280000")),
                        },
                    ],
                },
            ],
        },
        {
            "title_en": "Beresht House Menu",
            "title_fa": "منوی اصلی برشت",
            "subtitle_en": "Signature espresso service, day-long bites, and desserts.",
            "subtitle_fa": "اسپرسوهای امضایی، میان‌وعده‌ها و دسرها.",
            "menu_type": "main",
            "display_order": 2,
            "sections": [
                {
                    "title_en": "Signature Espresso Bar",
                    "title_fa": "بار امضای اسپرسو",
                    "section_type": "beverages",
                    "description_en": "The core beverages available throughout the day.",
                    "description_fa": "نوشیدنی‌های ثابت که تمام روز سرو می‌شوند.",
                    "items": [
                        {
                            "name_en": "Classic Beresht Espresso",
                            "name_fa": "اسپرسوی کلاسیک برشت",
                            "description_en": "House espresso blend dialed sweet with hints of cacao and cedar.",
                            "description_fa": "بلند اختصاصی با نت کاکائو و سرو.",
                            "item_type": "espresso",
                            "available_sizes": "Single,Double",
                            "spice_level": 0,
                            "is_featured": True,
                            **make_price_block(Decimal("160000")),
                        },
                        {
                            "name_en": "Pistachio Iced Latte",
                            "name_fa": "لته یخی پسته",
                            "description_en": "Double shot shaken with pistachio milk, cardamom bitters, honey.",
                            "description_fa": "دبل شات با شیر پسته، بیتر هل و عسل تکان داده شده.",
                            "item_type": "milk",
                            "available_sizes": "Double",
                            "spice_level": 1,
                            "is_vegetarian": True,
                            "contains_allergens": "nuts",
                            **make_price_block(Decimal("250000")),
                        },
                        {
                            "name_en": "Stone Flower Tea",
                            "name_fa": "چای گل‌سنگ",
                            "description_en": "House black tea infused with smoked lavender and bergamot.",
                            "description_fa": "چای سیاه با لاوندر دودی و ترنج.",
                            "item_type": "tea",
                            "available_sizes": "Pot",
                            "spice_level": 0,
                            "is_vegan": True,
                            **make_price_block(Decimal("150000")),
                        },
                    ],
                },
                {
                    "title_en": "Slow Morning Bites",
                    "title_fa": "لقمه‌های صبح‌آهسته",
                    "section_type": "food",
                    "description_en": "Baked goods and plates designed for pairing with espresso.",
                    "description_fa": "خوراکی‌هایی برای همراهی با اسپرسو.",
                    "items": [
                        {
                            "name_en": "Rose Pistachio Cruffin",
                            "name_fa": "کرافین پسته و رز",
                            "description_en": "Croissant muffin filled with rose pastry cream and pistachio brittle.",
                            "description_fa": "کرافین پر شده با کرم رز و بریتل پسته.",
                            "item_type": "food",
                            "spice_level": 0,
                            "is_vegetarian": True,
                            "contains_allergens": "gluten, dairy, eggs, nuts",
                            "preparation_time": 4,
                            **make_price_block(Decimal("210000")),
                        },
                        {
                            "name_en": "Smoked Trout Tartine",
                            "name_fa": "تارتین قزل‌آلای دودی",
                            "description_en": "Sourdough, smoked trout, dill labneh, shaved radish.",
                            "description_fa": "نان خمیرترش، قزل‌آلای دودی، لبنه شوید و تربچه.",
                            "item_type": "food",
                            "spice_level": 1,
                            "contains_allergens": "fish, dairy, gluten",
                            "preparation_time": 6,
                            **make_price_block(Decimal("370000")),
                        },
                        {
                            "name_en": "Charred Halloumi Bowl",
                            "name_fa": "بول هالومی کبابی",
                            "description_en": "Halloumi, roasted grape tomatoes, basil pesto grains.",
                            "description_fa": "هالومی، گوجه کبابی و غلات با پستو ریحان.",
                            "item_type": "food",
                            "spice_level": 1,
                            "is_vegetarian": True,
                            "contains_allergens": "dairy, nuts",
                            "preparation_time": 7,
                            **make_price_block(Decimal("330000")),
                        },
                    ],
                },
                {
                    "title_en": "Dessert Flight",
                    "title_fa": "پرواز دسر",
                    "section_type": "desserts",
                    "description_en": "Sweet bites balanced for coffee pairings.",
                    "description_fa": "دسرهایی برای همنشینی با قهوه.",
                    "items": [
                        {
                            "name_en": "Cold Brew Tiramisu Jar",
                            "name_fa": "تیرامیسو جار کلدو",
                            "description_en": "Classic tiramisu soaked with Beresht cold brew and cocoa nib dust.",
                            "description_fa": "تیرامیسو خیس خورده با کلدو برشت و غبار نیب کاکائو.",
                            "item_type": "dessert",
                            "spice_level": 0,
                            "contains_allergens": "dairy, gluten, eggs",
                            **make_price_block(Decimal("280000")),
                        },
                        {
                            "name_en": "Saffron Citrus Basque Cheesecake",
                            "name_fa": "چیزکیک باسکی زعفرانی",
                            "description_en": "Burnt cheesecake slice with saffron caramel and candied citrus strip.",
                            "description_fa": "چیزکیک سوخته با کارامل زعفرانی و پوست مرکبات قندی.",
                            "item_type": "dessert",
                            "spice_level": 0,
                            "contains_allergens": "dairy, eggs",
                            **make_price_block(Decimal("300000")),
                        },
                        {
                            "name_en": "Cardamom Cocoa Cookie",
                            "name_fa": "کوکی کاکائو و هل",
                            "description_en": "Thick chewy cookie with toasted cacao nibs and cardamom sugar.",
                            "description_fa": "کوکی ضخیم با نیب کاکائو تست و شکر هل.",
                            "item_type": "dessert",
                            "spice_level": 0,
                            "is_vegetarian": True,
                            "contains_allergens": "gluten, dairy, eggs",
                            **make_price_block(Decimal("150000")),
                        },
                    ],
                },
                {
                    "title_en": "Evening Savories",
                    "title_fa": "اسنک‌های عصرگاهی",
                    "section_type": "food",
                    "description_en": "Savory plates that pair with sunset espresso service.",
                    "description_fa": "خوردنی‌های شور برای سرو اسپرسو غروب.",
                    "items": [
                        {
                            "name_en": "Roasted Pepper Labneh Dip",
                            "name_fa": "دیپ لبنه فلفل برشته",
                            "description_en": "Creamy labneh, coal blistered peppers, and sesame flatbread chips.",
                            "description_fa": "لبنه خامه‌ای با فلفل‌های دودی و چیپس نان کنجدی.",
                            "item_type": "food",
                            "spice_level": 1,
                            "is_vegetarian": True,
                            "is_todays_special": True,
                            "contains_allergens": "dairy, gluten, sesame",
                            **make_price_block(Decimal("260000")),
                        },
                        {
                            "name_en": "Sumac Chicken Mini Toast",
                            "name_fa": "نان تست مرغ سماقی",
                            "description_en": "Shredded chicken dressed in sumac yogurt with pickled cucumbers.",
                            "description_fa": "مرغ ریش‌ریش با ماست سماقی و خیار ترشی روی نان.",
                            "item_type": "food",
                            "spice_level": 2,
                            "contains_allergens": "gluten, dairy",
                            "is_todays_special": False,
                            **make_price_block(Decimal("280000")),
                        },
                        {
                            "name_en": "Smoked Almond Date Roll",
                            "name_fa": "رول مغز بادام و خرما دودی",
                            "description_en": "Warm date rolls filled with smoked almond butter and citrus peel.",
                            "description_fa": "رول خرمای گرم با کره بادام دودی و پوست مرکبات.",
                            "item_type": "food",
                            "spice_level": 0,
                            "is_vegetarian": True,
                            "is_todays_special": True,
                            "contains_allergens": "nuts, gluten",
                            **make_price_block(Decimal("240000")),
                        },
                    ],
                },
            ],
        },
    ]


def create_menu(menu_def, menu_model, section_model, item_model, cover_field_name="cover_image"):
    menu_kwargs = {
        "title_en": menu_def["title_en"],
        "title_fa": menu_def["title_fa"],
        "subtitle_en": menu_def.get("subtitle_en"),
        "subtitle_fa": menu_def.get("subtitle_fa"),
        "menu_type": menu_def.get("menu_type", "main"),
        "display_order": menu_def.get("display_order", 0),
    }
    if hasattr(menu_model, "service_hours"):
        menu_kwargs["service_hours"] = menu_def.get("service_hours", "")
    if hasattr(menu_model, "valid_from") and menu_def.get("valid_from"):
        menu_kwargs["valid_from"] = menu_def.get("valid_from")
    if hasattr(menu_model, "valid_until") and menu_def.get("valid_until"):
        menu_kwargs["valid_until"] = menu_def.get("valid_until")

    menu = menu_model.objects.create(**menu_kwargs)
    cover_field = getattr(menu, cover_field_name, None)
    if cover_field:
        attach_random_image(cover_field, menu.title_en)
    sections_created = 0
    items_created = 0
    for sec_index, section_def in enumerate(menu_def["sections"], start=1):
        section_kwargs = {
            "menu": menu,
            "title_en": section_def["title_en"],
            "title_fa": section_def["title_fa"],
            "description_en": section_def.get("description_en", ""),
            "description_fa": section_def.get("description_fa", ""),
            "display_order": sec_index,
        }
        if hasattr(section_model, "section_type"):
            section_kwargs["section_type"] = section_def.get("section_type", "beverages")
        if hasattr(section_model, "meal_type"):
            section_kwargs["meal_type"] = section_def.get("meal_type", "any")
        section = section_model.objects.create(**section_kwargs)
        sections_created += 1
        for item_index, item_def in enumerate(section_def["items"], start=1):
            item_fields = {
                "section": section,
                "name_en": item_def["name_en"],
                "name_fa": item_def["name_fa"],
                "description_en": item_def.get("description_en", ""),
                "description_fa": item_def.get("description_fa", ""),
                "price": item_def["price"],
                "price_fa": item_def["price_fa"],
                "price_en": item_def["price_en"],
                "item_type": item_def.get("item_type", "main_course"),
                "cuisine_type": item_def.get("cuisine_type", "persian"),
                "ingredients_en": item_def.get("ingredients_en", ""),
                "ingredients_fa": item_def.get("ingredients_fa", ""),
                "cooking_method": item_def.get("cooking_method", ""),
                "serving_temperature": item_def.get("serving_temperature", ""),
                "spice_level": item_def.get("spice_level", 0),
                "portion_size": item_def.get("portion_size", ""),
                "is_vegetarian": item_def.get("is_vegetarian", False),
                "is_vegan": item_def.get("is_vegan", False),
                "is_gluten_free": item_def.get("is_gluten_free", False),
                "contains_allergens": item_def.get("contains_allergens", ""),
                "preparation_time": item_def.get("preparation_time"),
                "calories": item_def.get("calories"),
                "display_order": item_index,
                "is_available": item_def.get("is_available", True),
                "is_todays_special": item_def.get("is_todays_special", False),
                "is_featured": item_def.get("is_featured", False),
                "is_chefs_special": item_def.get("is_chefs_special", False),
                "popularity_score": item_def.get("popularity_score", 0),
            }

            if hasattr(item_model, "cuisine_type") is False:
                item_fields.pop("cuisine_type", None)
                item_fields.pop("cooking_method", None)
                item_fields.pop("serving_temperature", None)
                item_fields.pop("portion_size", None)
                item_fields.pop("is_chefs_special", None)
                item_fields.pop("popularity_score", None)

            if hasattr(item_model, "available_sizes") is False:
                item_fields.pop("available_sizes", None)
            else:
                item_fields["available_sizes"] = item_def.get("available_sizes", "")

            item = item_model.objects.create(**item_fields)
            attach_random_image(item.image, item.name_en)
            items_created += 1
    return sections_created, items_created


@transaction.atomic
def seed():
    BereshtMenu.objects.all().delete()
    MadiMenu.objects.all().delete()

    madi_sections = 0
    madi_items = 0
    for menu_payload in madi_menu_payloads():
        sec_count, item_count = create_menu(
            menu_payload,
            MadiMenu,
            MadiMenuSection,
            MadiMenuItem,
            cover_field_name="cover_image",
        )
        madi_sections += sec_count
        madi_items += item_count

    beresht_sections = 0
    beresht_items = 0
    for menu_payload in beresht_menu_payloads():
        sec_count, item_count = create_menu(
            menu_payload,
            BereshtMenu,
            BereshtMenuSection,
            BereshtMenuItem,
            cover_field_name="cover_image",
        )
        beresht_sections += sec_count
        beresht_items += item_count

    print(
        f"Seeded {MadiMenu.objects.count()} Madi menus with "
        f"{madi_sections} sections / {madi_items} items.",
    )
    print(
        f"Seeded {BereshtMenu.objects.count()} Beresht menus with "
        f"{beresht_sections} sections / {beresht_items} items.",
    )


if __name__ == "__main__":
    seed()
