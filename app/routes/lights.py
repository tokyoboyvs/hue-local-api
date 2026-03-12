from app.services.factory import get_hue_client
from app.config import settings
from fastapi import APIRouter

router = APIRouter(prefix='/lights', tags=['lights'])

@router.get('')
def get_light():
    client = get_hue_client()

    return {
        'mode': settings.APP_MODE,
        'items': client.get_lights()
    }
