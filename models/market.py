from typing import List

from pydantic import BaseModel

from .selection import Selection


class Market(BaseModel):
    '''Defines what kind of bets users can place'''
    id: int
    name: str
    selections: List[Selection]

    class Config:
        orm_mode = True
