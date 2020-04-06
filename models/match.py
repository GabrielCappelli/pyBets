from dataclasses import dataclass
from datetime import datetime
from typing import List

from .market import Market
from .sport import Sport


@dataclass
class Match():
    id: str
    url: str
    name: str
    startTime: datetime
    sport: Sport
    markets: List[Market]
