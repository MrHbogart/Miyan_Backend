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
        price_fa='120000',
        price_en='120000',
    )
    BereshtMenuItem.objects.create(
        section=inactive_section,
        name_fa='مخفی',
        name_en='Hidden',
        price_fa='50000',
        price_en='50000',
    )
    BereshtMenuItem.objects.create(
        section=section,
        name_fa='ناموجود',
        name_en='Unavailable',
        price_fa='80000',
        price_en='80000',
    )

    payload = BereshtMenuSerializer(instance=menu).data

    assert payload['title'] == {'fa': 'منو برشت', 'en': 'Beresht Menu'}
    assert payload['subtitle'] == {'fa': 'زیرعنوان', 'en': 'Subtitle'}
    assert len(payload['sections']) == 1
    assert payload['sections'][0]['title']['en'] == 'Coffee'
    # both items in the active section are exposed (availability flags removed)
    assert len(payload['sections'][0]['items']) == 2
    names = [it['name']['en'] for it in payload['sections'][0]['items']]
    assert 'Americano' in names and 'Unavailable' in names
    # prices are the formatted strings provided by the model
    fa_prices = [it['price']['fa'] for it in payload['sections'][0]['items']]
    assert '120000' in fa_prices and '80000' in fa_prices


@pytest.mark.django_db
def test_madi_menu_serializer_handles_breakfast_and_specials():
    menu = MadiMenu.objects.create(
        title_fa='منوی مادی',
        title_en='Madi Menu',
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
        price_fa='250000',
        price_en='250000',
    )
    MadiMenuItem.objects.create(
        section=section,
        name_fa='فرنچ تست',
        name_en='French Toast',
        price_fa='300000',
        price_en='300000',
    )

    payload = MadiMenuSerializer(instance=menu).data

    assert payload['title']['en'] == 'Madi Menu'
    assert len(payload['sections']) == 1
    assert len(payload['sections'][0]['items']) == 2
