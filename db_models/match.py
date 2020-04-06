from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from database import Base

from .market import Market
from .sport import Sport


class Match(Base):
    '''Match ORM definition'''

    __tablename__ = 'match'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    name = Column(String, index=True)
    startTime = Column(DateTime, index=True)
    sport_id = Column(Integer, ForeignKey(Sport.id))
    sport = relationship("Sport")
    markets = relationship("Market", secondary='match_markets')


match_markets_tbl = Table(
    'match_markets', Base.metadata,
    Column('match_id', Integer, ForeignKey(Match.id)),
    Column('market_id', Integer, ForeignKey(Market.id))
)
