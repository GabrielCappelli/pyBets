from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

from .sport import Sport


class Market(Base):
    '''Market ORM definition'''

    __tablename__ = 'market'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    selections = relationship("Selection")
    sport_id = Column(Integer, ForeignKey(Sport.id))
