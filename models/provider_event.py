from pydantic import BaseModel

from .match import Match


class ProviderEvent(BaseModel):
    '''Data sent by providers to update matches in realtime'''
    id: int
    message_type: str
    event: Match
