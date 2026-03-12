from app.models import BridgeStatusResponse, BrightnessUpdateRequest, BulkLightActionRequest, BulkLightActionResponse, ColorUpdateRequest, LightActionResponse, LightDetailsResponse, LightsListResponse
from app.exceptions import HueBridgeAuthenticationError, HueBridgeConnectionError, HueBridgeNotConfiguredError, HueResourceNotFoundError
from app.services.factory import get_hue_client
from fastapi import APIRouter, HTTPException
from app.config import settings

router = APIRouter(prefix='/lights', tags=['lights'])


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


@router.get('/bridge/status', response_model=BridgeStatusResponse)
def get_bridge_status():
    client = get_hue_client()

    if settings.APP_MODE == 'mock':
        return {
            'mode': settings.APP_MODE,
            'bridge_configured': False,
            'bridge_reachable': False
        }
    
    try:
        return {
            'mode': settings.APP_MODE,
            'bridge_configured': client.is_configured(),
            'bridge_reachable': client.check_bridge_connection()
        }
    except (
        HueBridgeAuthenticationError,
        HueBridgeConnectionError,
        HueBridgeNotConfiguredError,
        HueResourceNotFoundError
    ) as exc:
        handle_hue_error(exc)


@router.get('', response_model=LightsListResponse)
def get_lights():
    client = get_hue_client()

    try:
        return {
            'mode': settings.APP_MODE,
            'items': client.get_lights()
        }
    except (
        HueBridgeAuthenticationError,
        HueBridgeConnectionError,
        HueBridgeNotConfiguredError,
        HueResourceNotFoundError
    ) as exc:
        handle_hue_error(exc)


@router.post('/actions/on', response_model=BulkLightActionResponse)
def bulk_turn_on_lights(payload: BulkLightActionRequest):
    client = get_hue_client()
    updated_lights, missing_light_ids = client.bulk_turn_on_lights(payload.light_ids)

    return {
        'success': True,
        'message': 'Bulk on action executed',
        'updated_lights': updated_lights,
        'missing_light_ids': missing_light_ids
    }


@router.post('/actions/off', response_model=BulkLightActionResponse)
def bulk_turn_off_lights(payload: BulkLightActionRequest):
    client = get_hue_client()
    updated_lights, missing_light_ids = client.bulk_turn_off_lights(payload.light_ids)

    return {
        'success': True,
        'message': 'Bulk off action executed',
        'updated_lights': updated_lights,
        'missing_light_ids': missing_light_ids
    }


@router.post('/actions/toggle', response_model=BulkLightActionResponse)
def bulk_toggle_lights(payload: BulkLightActionRequest):
    client = get_hue_client()
    updated_lights, missing_light_ids = client.bulk_toggle_lights(payload.light_ids)

    return {
        'success': True,
        'message': 'Bulk toggle action executed',
        'updated_lights': updated_lights,
        'missing_light_ids': missing_light_ids
    }


@router.get('/{light_id}', response_model=LightDetailsResponse)
def get_light(light_id: str):
    client = get_hue_client()

    try:
        light = client.get_light_by_id(light_id)
    except (
        HueBridgeAuthenticationError,
        HueBridgeConnectionError,
        HueBridgeNotConfiguredError,
        HueResourceNotFoundError
    ) as exc:
        handle_hue_error(exc)

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

    try:
        light = client.turn_on_light(light_id)
    except (
        HueBridgeAuthenticationError,
        HueBridgeConnectionError,
        HueBridgeNotConfiguredError,
        HueResourceNotFoundError
    ) as exc:
        handle_hue_error(exc)

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

    try:
        light = client.turn_off_light(light_id)
    except (
        HueBridgeAuthenticationError,
        HueBridgeConnectionError,
        HueBridgeNotConfiguredError,
        HueResourceNotFoundError
    ) as exc:
        handle_hue_error(exc)

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

    try:
        light = client.toggle_light(light_id)
    except (
        HueBridgeAuthenticationError,
        HueBridgeConnectionError,
        HueBridgeNotConfiguredError,
        HueResourceNotFoundError
    ) as exc:
        handle_hue_error(exc)

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

    try: 
        light = client.set_brightness(light_id, payload.brightness)
    except (
        HueBridgeAuthenticationError,
        HueBridgeConnectionError,
        HueBridgeNotConfiguredError,
        HueResourceNotFoundError
    ) as exc:
        handle_hue_error(exc)

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
    
    try:
        light = client.set_color(light_id, payload.color)
    except (
        HueBridgeAuthenticationError,
        HueBridgeConnectionError,
        HueBridgeNotConfiguredError,
        HueResourceNotFoundError
    ) as exc:
        handle_hue_error(exc)

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
