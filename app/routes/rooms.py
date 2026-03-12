from app.models import LightModel, LightsListResponse, RoomModel, RoomsListResponse
from app.services.factory import get_hue_client
from fastapi import APIRouter, HTTPException
from app.config import settings

router = APIRouter(prefix='/rooms', tags=['rooms'])


@router.get('', response_model=RoomsListResponse)
def get_rooms():
    client = get_hue_client()

    return {
        'mode': settings.APP_MODE,
        'items': client.get_rooms()
    }


@router.get('/{room_name}/lights', response_model=LightsListResponse)
def get_room_lights(room_name: str):
    client = get_hue_client()
    lights = client.get_lights_by_room(room_name)

    if not lights:
        raise HTTPException(
            status_code=404,
            detail=f'Room \'{room_name}\' not found'
        )
    
    return {
        'mode': settings.APP_MODE,
        'items': lights
    }
