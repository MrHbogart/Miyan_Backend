import pytest
from django.urls import reverse

from miyanBeresht.models import BereshtMenu
pytestmark = pytest.mark.django_db


def _create_menu(**overrides):
    data = {
        'title_fa': 'منو',
        'title_en': 'Menu',
        'subtitle_fa': '',
        'subtitle_en': '',
    }
    data.update(overrides)
    return BereshtMenu.objects.create(**data)


def _list_menus(client):
    url = reverse('beresht-menu-list')
    response = client.get(url)
    assert response.status_code == 200
    return response.json()


def test_public_menu_list_hides_inactive(client):
    _create_menu(title_en='Public Menu', is_active=True)
    _create_menu(title_en='Inactive Menu', is_active=False)

    payload = _list_menus(client)

    assert len(payload) == 1
    assert payload[0]['title']['en'] == 'Public Menu'


def test_staff_menu_list_includes_inactive(client, django_user_model):
    _create_menu(title_en='Active Menu', is_active=True)
    _create_menu(title_en='Inactive Menu', is_active=False)

    user = django_user_model.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='pass',
        is_staff=True,
    )
    client.force_login(user)

    payload = _list_menus(client)

    assert len(payload) == 2
    assert {entry['title']['en'] for entry in payload} == {
        'Active Menu',
        'Inactive Menu',
    }
