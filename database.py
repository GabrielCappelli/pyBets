from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request

DATABASE_URL = "sqlite:///database.db"

engine = create_engine(DATABASE_URL, echo=True,)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_request_session(request: Request):
    return request.state.db_session
