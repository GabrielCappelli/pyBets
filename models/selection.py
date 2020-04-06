from pydantic import BaseModel


class Selection(BaseModel):
    '''Players/teams odds in a Match'''
    id: str
    name: str
    odds: float
