from sqlalchemy import Column, Float, ForeignKey, Integer, String

from database import Base

from .market import Market


class Selection(Base):
    '''Selection ORM definition'''

    __tablename__ = 'selection'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    odds = Column(Float)
    market_id = Column(Integer, ForeignKey(Market.id))
