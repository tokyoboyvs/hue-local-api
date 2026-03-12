import httpx


class HueClient:
    def __init__(self, bridge_ip: str, app_key: str):
        self.bridge_ip = bridge_ip
        self.app_key = app_key
        self.base_url = f'https://{bridge_ip}/clip/v2' if bridge_ip else ''


    def is_configured(self):
        return bool(self.bridge_ip and self.app_key)


    def get_headers(self):
        return {
            'hue-application-key': self.app_key
        }
    

    def _get(self, path: str):
        if not self.is_configured():
            return []
        
        try:
            response = httpx.get(
                f'{self.base_url}{path}',
                headers=self.get_headers(),
                timeout=5.0,
                verify=False
            )
            response.raise_for_status()
            payload = response.json()
            return payload.get('data', [])
        except (httpx.HTTPError, ValueError):
            return []
    

    def _put(self, path: str, data: dict):
        if not self.is_configured():
            return False
        
        try:
            response = httpx.put(
                f'{self.base_url}{path}',
                headers=self.get_headers(),
                json=data,
                timeout=5.0,
                verify=False
            )
            response.raise_for_status()
            return True
        except httpx.HTTPError:
            return False
    

    def _extract_brightness(self, raw_light: dict):
        dimming = raw_light.get('dimming')
        if not dimming:
            return 0

        brightness = dimming.get('brightness', 0)
        return int(round(brightness))
    

    def _extract_color(self, raw_light: dict):
        color = raw_light.get('color')
        if color:
            return '#FFFFFF'

        return '#FFFFFF'
    

    def _map_light(self, raw_light: dict):
        metadata = raw_light.get('metadata', {})
        on_data = raw_light.get('on', {})

        return {
            'id': raw_light.get('id', ''),
            'name': metadata.get('name', raw_light.get('id', 'unknown-light')),
            'room': 'unknown',
            'is_on': on_data.get('on', False),
            'brightness': self._extract_brightness(raw_light),
            'color': self._extract_color(raw_light)
        }


    def check_bridge_connection(self):
        if not self.is_configured():
            return False
        
        try:
            response = httpx.get(
                f'{self.base_url}/resource/device',
                headers=self.get_headers(),
                timeout=5.0,
                verify=False
            )
            return response.status_code == 200
        except httpx.HTTPError:
            return False


    def get_lights(self):
        return []


    def get_light_by_id(self, light_id: str):
        return None


    def turn_on_light(self, light_id: str):
        light = self.get_light_by_id(light_id)
        if light is None:
            return None
        
        success = self._put(f'/resource/light/{light_id}', {'on': {'on': True}})
        if not success:
            return None
        
        light['is_on'] = True
        return light


    def turn_off_light(self, light_id: str):
        light = self.get_light_by_id(light_id)
        if light is None:
            return None
        
        success = self._put(f'/resource/light/{light_id}', {'on': {'on': False}})
        if not success:
            return None
        
        light['is_on'] = False
        return light


    def toggle_light(self, light_id: str):
        light = self.get_light_by_id(light_id)
        if light is None:
            return None
        
        if light['is_on']:
            return self.turn_off_light(light_id)
        
        return self.turn_on_light(light_id)


    def set_brightness(self, light_id: str, brightness: int):
        return None


    def set_color(self, light_id: str, color: str):
        return None


    def get_rooms(self):
        return []


    def get_lights_by_room(self, room_name: str):
        return []


    def bulk_turn_on_lights(self, light_ids: list[str]):
        return [], []


    def bulk_turn_off_lights(self, light_ids: list[str]):
        return [], []
    

    def bulk_toggle_lights(self, light_ids: list[str]):
        return [], []
