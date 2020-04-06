from typing import List

from pydantic import BaseModel

from .selection import Selection


class Market(BaseModel):
    '''Defines what kind of bets users can place'''
    id: str
    name: str
    selections: List[Selection]
