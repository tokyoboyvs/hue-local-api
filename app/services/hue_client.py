class HueClient:
    def __init__(self, bridge_ip: str, app_key: str):
        self.bridge_ip = bridge_ip
        self.app_key = app_key
    
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
