from dataclasses import dataclass
from typing import List

from .selection import Selection


@dataclass
class Market():
    id: str
    name: str
    selections: List[Selection]
