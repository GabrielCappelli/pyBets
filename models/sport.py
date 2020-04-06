from pydantic import BaseModel


class Sport(BaseModel):
    '''Sport data'''
    id: int
    name: str

    class Config:
        orm_mode = True
