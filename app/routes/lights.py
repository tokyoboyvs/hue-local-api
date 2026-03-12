from app.services.factory import get_hue_client
from app.models import LightsListResponse
from app.config import settings
from fastapi import APIRouter

router = APIRouter(prefix='/lights', tags=['lights'])

@router.get('', response_model=LightsListResponse)
def get_light():
    client = get_hue_client()

    return {
        'mode': settings.APP_MODE,
        'items': client.get_lights()
    }
