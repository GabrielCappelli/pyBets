from typing import List

from fastapi import APIRouter, Depends, HTTPException

from database import Session, get_request_session
from models import Match
from services.match import get_match, get_matches

match_router = APIRouter()


@match_router.get('/', response_model=List[Match])
async def get_matches_route() -> List[Match]:
    '''Gets the list of matches that match the user parameters

    Returns:
        List[Match]: List of matches matching user parameters
    '''
    return []


@match_router.get('/{match_id}', response_model=Match)
async def get_match_route(match_id: int, db_session: Session = Depends(get_request_session)) -> List[Match]:
    '''Gets the list of matches that match the user parameters

    Returns:
        List[Match]: List of matches matching user parameters
    '''
    try:
        return get_match(match_id, db_session)
    except ValueError as ex:
        raise HTTPException(422, str(ex))
    except Exception as ex:
        raise HTTPException(500, str(ex))
