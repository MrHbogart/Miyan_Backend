from decimal import Decimal

import pytest

from miyanBeresht.models import BereshtMenu, BereshtMenuItem, BereshtMenuSection
from miyanBeresht.serializers import BereshtMenuSerializer
from miyanMadi.models import MadiMenu, MadiMenuItem, MadiMenuSection
from miyanMadi.serializers import MadiMenuSerializer


@pytest.mark.django_db
def test_beresht_menu_serializer_shapes_public_payload():
    menu = BereshtMenu.objects.create(
        title_fa='منو برشت',
        title_en='Beresht Menu',
        subtitle_fa='زیرعنوان',
        subtitle_en='Subtitle',
    )
    section = BereshtMenuSection.objects.create(
        menu=menu,
        title_fa='قهوه',
        title_en='Coffee',
        is_active=True,
    )
    inactive_section = BereshtMenuSection.objects.create(
        menu=menu,
        title_fa='غیرفعال',
        title_en='Inactive',
        is_active=False,
    )
    BereshtMenuItem.objects.create(
        section=section,
        name_fa='آمریکانو',
        name_en='Americano',
        description_fa='',
        description_en='',
        price=Decimal('120000'),
        price_fa='120000',
        price_en='120000',
        is_available=True,
        is_todays_special=True,
    )
    BereshtMenuItem.objects.create(
        section=inactive_section,
        name_fa='مخفی',
        name_en='Hidden',
        price=Decimal('50000'),
        price_fa='50000',
        price_en='50000',
        is_available=True,
    )
    BereshtMenuItem.objects.create(
        section=section,
        name_fa='ناموجود',
        name_en='Unavailable',
        price=Decimal('80000'),
        price_fa='80000',
        price_en='80000',
        is_available=False,
    )

    payload = BereshtMenuSerializer(instance=menu).data

    assert payload['title'] == {'fa': 'منو برشت', 'en': 'Beresht Menu'}
    assert payload['subtitle'] == {'fa': 'زیرعنوان', 'en': 'Subtitle'}
    assert len(payload['sections']) == 1
    assert payload['sections'][0]['title']['en'] == 'Coffee'
    assert len(payload['sections'][0]['items']) == 1
    item = payload['sections'][0]['items'][0]
    assert item['name']['en'] == 'Americano'
    assert item['price']['fa'] == '120'
    todays = payload['todays']['sections'][0]['items']
    assert len(todays) == 1
    assert todays[0]['name']['en'] == 'Americano'


@pytest.mark.django_db
def test_madi_menu_serializer_handles_breakfast_and_specials():
    menu = MadiMenu.objects.create(
        title_fa='منوی مادی',
        title_en='Madi Menu',
        menu_type='breakfast',
        service_hours='7am - 11am',
    )
    section = MadiMenuSection.objects.create(
        menu=menu,
        title_fa='صبحانه',
        title_en='Breakfast',
        meal_type='breakfast',
    )
    MadiMenuItem.objects.create(
        section=section,
        name_fa='املت',
        name_en='Omelette',
        price=Decimal('250000'),
        price_fa='250000',
        price_en='250000',
        is_available=True,
        is_todays_special=True,
        is_featured=True,
    )
    MadiMenuItem.objects.create(
        section=section,
        name_fa='فرنچ تست',
        name_en='French Toast',
        price=Decimal('300000'),
        price_fa='300000',
        price_en='300000',
        is_available=True,
        is_todays_special=False,
    )

    payload = MadiMenuSerializer(instance=menu).data

    assert payload['title']['en'] == 'Madi Menu'
    assert len(payload['sections']) == 1
    assert len(payload['sections'][0]['items']) == 2
    todays_items = payload['todays']['sections'][0]['items']
    assert [item['name']['en'] for item in todays_items] == ['Omelette']
