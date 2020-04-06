from sqlalchemy import Column, Integer, String

from database import Base


class Sport(Base):
    '''Sport data'''

    __tablename__ = 'sport'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
