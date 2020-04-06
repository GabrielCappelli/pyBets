from datetime import datetime
from typing import List

from pydantic import BaseModel

from .market import Market
from .sport import Sport


class Match(BaseModel):
    '''Defines a Match users can bet on'''
    id: str
    url: str
    name: str
    startTime: datetime
    sport: Sport
    markets: List[Market]
