from dataclasses import dataclass

from .match import Match


@dataclass
class ProviderEvent():
    '''External provider`s data format'''
    id: int
    message_type: str
    event: Match
