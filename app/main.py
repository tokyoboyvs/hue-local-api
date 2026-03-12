from app.routes.lights import router as lights_router
from app.routes.rooms import router as rooms_router
from app.dependencies import require_api_key
from app.models import HealthResponse
from fastapi import Depends, FastAPI
from app.config import settings

app = FastAPI(
    title='Hue Local API',
    version='0.1.0'
)

app.include_router(
    lights_router,
    prefix='/api',
    dependencies=[Depends(require_api_key)]
)
app.include_router(
    rooms_router,
    prefix='/api',
    dependencies=[Depends(require_api_key)]
)


@app.get('/health', response_model=HealthResponse)
def health():
    return {
        'status': 'ok',
        'app': 'hue-local-api',
        'version': '0.1.0',
        'mode': settings.APP_MODE
    }
