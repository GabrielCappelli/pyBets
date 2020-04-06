from pydantic import BaseModel


class Selection(BaseModel):
    '''Players/teams odds in a Match'''
    id: int
    name: str
    odds: float

    class Config:
        orm_mode = True
