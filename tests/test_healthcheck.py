import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_health_endpoint(client, settings):
    url = reverse('core-health')
    response = client.get(url)
    assert response.status_code == 200
    payload = response.json()
    assert payload['status'] == 'ok'
    assert payload['version'] == settings.APP_VERSION
    assert payload['revision'] == settings.APP_COMMIT_SHA
