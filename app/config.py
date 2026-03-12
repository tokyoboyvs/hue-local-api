from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    APP_MODE: str = os.getenv('APP_MODE', 'mock').strip().lower()
    HUE_BRIDGE_IP: str = os.getenv('HUE_BRIDGE_IP', '').strip()
    HUE_APP_KEY: str = os.getenv('HUE_APP_KEY', '').strip()
    API_KEY: str = os.getenv('API_KEY', '').strip()

settings = Settings()
