class HueClient:
    def __init__(self, bridge_ip: str, app_key: str):
        self.bridge_ip = bridge_ip
        self.app_key = app_key
    
    def get_lights(self):
        return []
    
    def get_light_by_id(self, light_id: str):
        return None
