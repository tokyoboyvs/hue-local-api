import uvicorn
import os

if __name__ == '__main__':
    app_host = os.getenv('APP_HOST', '0.0.0.0')
    app_port = int(os.getenv('APP_PORT', '8000'))
    app_reload = os.getenv('APP_RELOAD', 'true').lower() == 'true'

    uvicorn.run(
        'app.main:app',
        host=app_host,
        port=app_port,
        reload=app_reload
    )
