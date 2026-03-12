from app.models import BridgeStatusResponse, BrightnessUpdateRequest, ColorUpdateRequest, LightActionResponse, LightDetailsResponse, LightsListResponse
from app.services.factory import get_hue_client
from fastapi import APIRouter, HTTPException
from app.config import settings

router = APIRouter(prefix='/lights', tags=['lights'])


@router.get('', response_model=LightsListResponse)
def get_lights():
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


@router.post('/{light_id}/on', response_model=LightActionResponse)
def turn_on_light(light_id: str):
    client = get_hue_client()
    light = client.turn_on_light(light_id)

    if light is None:
        raise HTTPException(
            status_code=404,
            detail=f'Light \'{light_id}\' not found'
        )
    
    return {
        'success': True,
        'message': f'Light \'{light_id}\' turned on',
        'light': light
    }


@router.post('/{light_id}/off', response_model=LightActionResponse)
def turn_off_light(light_id: str):
    client = get_hue_client()
    light = client.turn_off_light(light_id)

    if light is None:
        raise HTTPException(
            status_code=404,
            detail=f'Light \'{light_id}\' not found'
        )
    
    return {
        'success': True,
        'message': f'Light \'{light_id}\' turned off',
        'light': light
    }


@router.post('/{light_id}/toggle', response_model=LightActionResponse)
def toggle_light(light_id: str):
    client = get_hue_client()
    light = client.toggle_light(light_id)

    if light is None:
        raise HTTPException(
            status_code=404,
            detail=f'Light \'{light_id}\' not found'
        )
    
    return {
        'success': True,
        'message': f'Light \'{light_id}\' toggled',
        'light': light
    }


@router.post('/{light_id}/brightness', response_model=LightActionResponse)
def set_light_brightness(light_id: str, payload: BrightnessUpdateRequest):
    client = get_hue_client()
    light = client.set_brightness(light_id, payload.brightness)

    if light is None:
        raise HTTPException(
            status_code=404,
            detail=f'Light \'{light_id}\' not found'
        )
    
    return {
        'success': True,
        'message': f'Light \'{light_id}\' brightness set to {payload.brightness}',
        'light': light
    }


@router.post('/{light_id}/color', response_model=LightActionResponse)
def set_light_color(light_id: str, payload: ColorUpdateRequest):
    client = get_hue_client()
    light = client.set_color(light_id, payload.color)

    if light is None:
        raise HTTPException(
            status_code=404,
            detail=f'Light \'{light_id}\' not found'
        )
    
    return {
        'success': True,
        'message': f'Light \'{light_id}\' color set to {payload.color}',
        'light': light
    }


@router.get('/bridge/status', response_model=BridgeStatusResponse)
def get_bridge_status():
    client = get_hue_client()

    if settings.APP_MODE == 'mock':
        return {
            'mode': settings.APP_MODE,
            'bridge_configured': False,
            'bridge_reachable': False
        }
    
    return {
        'mode': settings.APP_MODE,
        'bridge_configured': client.is_configured(),
        'bridge_reachable': client.check_bridge_connection()
    }
