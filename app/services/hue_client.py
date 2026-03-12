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
        return None


    def turn_off_light(self, light_id: str):
        return None


    def toggle_light(self, light_id: str):
        return None


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
