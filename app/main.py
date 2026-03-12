from app.routes.lights import router as lights_router
from app.config import settings
from fastapi import FastAPI

app = FastAPI(
    title='Hue Local API',
    version='0.1.0'
)

app.include_router(lights_router, prefix='/api')

@app.get('/health')
def health():
    return {
        'status': 'ok',
        'app': 'hue-local-api',
        'version': '0.1.0',
        'mode': settings.APP_MODE
    }
