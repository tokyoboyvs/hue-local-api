from app.exceptions import HueBridgeAuthenticationError, HueBridgeConnectionError, HueBridgeNotConfiguredError, HueResourceNotFoundError
from app.models import LightModel, LightsListResponse, RoomModel, RoomsListResponse
from app.services.factory import get_hue_client
from fastapi import APIRouter, HTTPException
from app.config import settings

router = APIRouter(prefix='/rooms', tags=['rooms'])


def handle_hue_error(exc: Exception):
    if isinstance(exc, HueBridgeNotConfiguredError):
        raise HTTPException(status_code=500, detail='Hue Bridge is not configured')
    
    if isinstance(exc, HueBridgeAuthenticationError):
        raise HTTPException(status_code=502, detail='Hue Bridge authentication failed')
    
    if isinstance(exc, HueBridgeConnectionError):
        raise HTTPException(status_code=502, detail='Hue Bridge is unreachable')
    
    if isinstance(exc, HueResourceNotFoundError):
        raise HTTPException(status_code=404, detail='Hue resource not found')
    
    raise exc


@router.get('', response_model=RoomsListResponse)
def get_rooms():
    client = get_hue_client()

    try:
        return {
            'mode': settings.APP_MODE,
            'items': client.get_rooms()
        }
    except (
        HueBridgeAuthenticationError,
        HueBridgeConnectionError,
        HueBridgeNotConfiguredError,
        HueResourceNotFoundError
    ) as exc:
        handle_hue_error(exc)


@router.get('/{room_name}/lights', response_model=LightsListResponse)
def get_room_lights(room_name: str):
    client = get_hue_client()
    
    try:
        lights = client.get_lights_by_room(room_name)
    except (
        HueBridgeAuthenticationError,
        HueBridgeConnectionError,
        HueBridgeNotConfiguredError,
        HueResourceNotFoundError
    ) as exc:
        handle_hue_error(exc)

    if not lights:
        raise HTTPException(
            status_code=404,
            detail=f'Room \'{room_name}\' not found'
        )
    
    return {
        'mode': settings.APP_MODE,
        'items': lights
    }
