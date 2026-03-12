from app.services.mock_hue_client import MockHueClient
from app.services.hue_client import HueClient
from app.config import settings

_mock_client = MockHueClient()

def get_hue_client():
    if settings.APP_MODE == 'mock':
        return _mock_client

    return HueClient(
        bridge_ip=settings.HUE_BRIDGE_IP,
        app_key=settings.HUE_APP_KEY
    )
