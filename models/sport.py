from pydantic import BaseModel


class Sport(BaseModel):
    '''Sport data'''
    id: str
    name: str
