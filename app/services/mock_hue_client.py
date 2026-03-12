class MockHueClient:
    def __init__(self):
        self.lights = [
            {
                'id': 'light-1',
                'name': 'Desk Lamp',
                'room': 'office',
                'is_on': True,
                'brightness': 75,
                'color': '#FFD47A'
            },
            {
                'id': 'light-2',
                'name': 'Bed Light',
                'room': 'bedroom',
                'is_on': False,
                'brightness': 40,
                'color': '#FF66CC'
            }
        ]
    
    def get_lights(self):
        return self.lights
    
    def get_light_by_id(self, light_id: str):
        for light in self.lights:
            if light['id'] == light_id:
                return light
            
        return None
    
    def turn_on_light(self, light_id: str):
        light = self.get_light_by_id(light_id)
        if light is None:
            return None
        
        light['is_on'] = True
        return light
        
    def turn_off_light(self, light_id: str):
        light = self.get_light_by_id(light_id)
        if light is None:
            return None
        
        light['is_on'] = False
        return light
    
    def toggle_light(self, light_id: str):
        light = self.get_light_by_id(light_id)
        if light is None:
            return None
        
        light['is_on'] = not light['is_on']
        return light
    
    def set_brightness(self, light_id: str, brightness: int):
        light = self.get_light_by_id(light_id)
        if light is None:
            return None
        
        light['brightness'] = brightness
        return light
    
    def set_color(self, light_id: str, color: str):
        light = self.get_light_by_id(light_id)
        if light is None:
            return None
        
        light['color'] = color
        return light
