from typing import List

from fastapi import APIRouter

from models import Match

match_router = APIRouter()


@match_router.get('/', response_model=List[Match])
async def get_matches_route() -> List[Match]:
    '''Gets the list of matches that match the user parameters

    Returns:
        List[Match]: List of matches matching user parameters
    '''
    return []
