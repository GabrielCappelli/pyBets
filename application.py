from fastapi import FastAPI

from views import match_router, provider_router


def create_app() -> FastAPI:
    '''Creates FastAPI application and configures everything the application requires

    Returns:
        FastAPI: FastAPI ASGI object
    '''
    app = FastAPI()
    app.include_router(match_router, prefix='/match')
    app.include_router(provider_router, prefix='/provider')
    return app
