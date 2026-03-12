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
    
    
    def get_rooms(self):
        rooms = {}

        for light in self.lights:
            room_name = light['room']

            if room_name not in rooms:
                rooms[room_name] = 0
            
            rooms[room_name] += 1
        
        return [
            {
                'name': room_name,
                'light_count': light_count
            }
            for room_name, light_count in rooms.items()
        ]
    
    
    def get_lights_by_room(self, room_name: str):
        return [
            light for light in self.lights
            if light['room'] == room_name
        ]
    
    
    def is_configured(self):
        return False

    
    def check_bridge_connection(self):
        return False
    

    def bulk_turn_on_lights(self, light_ids: list[str]):
        updated_lights = []
        missing_light_ids = []

        for light_id in light_ids:
            light = self.turn_on_light(light_id)
            if light is None:
                missing_light_ids.append(light_id)
            else:
                updated_lights.append(light)

        return updated_lights, missing_light_ids


    def bulk_turn_off_lights(self, light_ids: list[str]):
        updated_lights = []
        missing_light_ids = []

        for light_id in light_ids:
            light = self.turn_off_light(light_id)
            if light is None:
                missing_light_ids.append(light_id)
            else:
                updated_lights.append(light)
            
        return updated_lights, missing_light_ids


    def bulk_toggle_lights(self, light_ids: list[str]):
        updated_lights = []
        missing_light_ids = []

        for light_id in light_ids:
            light = self.toggle_light(light_id)
            if light is None:
                missing_light_ids.append(light_id)
            else:
                updated_lights.append(light)
            
        return updated_lights, missing_light_ids
