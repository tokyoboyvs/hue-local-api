from app.services.factory import _mock_client
from fastapi.testclient import TestClient
from app.config import settings
from app.main import app


client = TestClient(app)


def reset_mock_lights():
    _mock_client.lights = [
        {
            'id': 'light-1',
            'name': 'Desk Lamp',
            'room': 'office',
            'is_on': True,
            'brightness': 75,
            'color': '#FFD47A'
        },
        {
            'id': 'light-2',
            'name': 'Bed Light',
            'room': 'bedroom',
            'is_on': False,
            'brightness': 40,
            'color': '#FF66CC'
        }
    ]


def api_headers():
    return {'X-API-Key' : 'test-key'}


def setup_function():
    settings.APP_MODE = 'mock'
    settings.API_KEY = 'test-key'
    reset_mock_lights()


def test_health_is_public():
    response = client.get('/health')

    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_get_lights_requires_api_key():
    response = client.get('/api/lights')

    assert response.status_code == 401
    assert response.json() == {'detail': 'Invalid or missing API key'}


def test_get_lights_returns_items():
    response = client.get('/api/lights', headers=api_headers())

    assert response.status_code == 200
    assert len(response.json()['items']) == 2


def test_toggle_light_updates_state():
    response = client.post('/api/lights/light-1/toggle', headers=api_headers())

    assert response.status_code == 200
    assert response.json()['light']['is_on'] is False


def test_set_brightness_updates_light():
    response = client.post(
        '/api/lights/light-1/brightness',
        headers=api_headers(),
        json={'brightness': 20}
    )

    assert response.status_code == 200
    assert response.json()['light']['brightness'] == 20


def test_set_brightness_rejects_invalid_value():
    response = client.post(
        '/api/lights/light-1/brightness',
        headers=api_headers(),
        json={'brightness': 101}
    )

    assert response.status_code == 422


def test_set_color_updates_light():
    response = client.post(
        '/api/lights/light-1/color',
        headers=api_headers(),
        json={'color': '#00FFAA'}
    )

    assert response.status_code == 200
    assert response.json()['light']['color'] == '#00FFAA'


def test_get_rooms_returns_items():
    response = client.get('/api/rooms', headers=api_headers())

    assert response.status_code == 200
    assert len(response.json()['items']) == 2


def test_get_room_lights_returns_room_items():
    response = client.get('/api/rooms/office/lights', headers=api_headers())

    assert response.status_code == 200
    assert len(response.json()['items']) == 1
    assert response.json()['items'][0]['room'] == 'office'


def test_unknown_room_returns_404():
    response = client.get('/api/rooms/kitchen/lights', headers=api_headers())

    assert response.status_code == 404
    assert response.json() == {'detail': "Room 'kitchen' not found"}
