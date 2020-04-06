from fastapi import FastAPI
from starlette.requests import Request

import database
from views import match_router, provider_router


def create_app() -> FastAPI:
    '''Creates FastAPI application and configures everything the application requires

    Returns:
        FastAPI: FastAPI ASGI object
    '''
    app = FastAPI()
    app.include_router(match_router, prefix='/api/match')
    app.include_router(provider_router, prefix='/api/provider')

    # TODO Replace this with alembic for db migrations
    database.Base.metadata.create_all(bind=database.engine)

    @app.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        request.state.db_session = database.Session()
        response = await call_next(request)
        request.state.db_session.close()
        return response

    return app
