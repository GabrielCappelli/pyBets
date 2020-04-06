from dataclasses import dataclass


@dataclass
class Selection():
    '''Players/teams odds in a Match'''
    id: str
    name: str
    odds: float
