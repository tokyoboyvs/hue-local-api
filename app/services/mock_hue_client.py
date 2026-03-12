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
