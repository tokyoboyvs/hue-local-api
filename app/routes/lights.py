from app.services.factory import get_hue_client
from app.models import LightDetailsResponse, LightsListResponse
from app.config import settings
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix='/lights', tags=['lights'])


@router.get('', response_model=LightsListResponse)
def get_light():
    client = get_hue_client()

    return {
        'mode': settings.APP_MODE,
        'items': client.get_lights()
    }


@router.get('/{light_id}', response_model=LightDetailsResponse)
def get_light(light_id: str):
    client = get_hue_client()
    light = client.get_light_by_id(light_id)

    if light is None:
        raise HTTPException(
            status_code=404,
            detail=f'Light \'{light_id}\' not found'
        )
    
    return {
        'mode': settings.APP_MODE,
        'item': light
    }
