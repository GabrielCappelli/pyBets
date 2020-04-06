from typing import List

from sqlalchemy import exc

import db_models
import error_messages
from app_logging import logger
from database import Session
from models import Match, ProviderEvent, Sport


def get_match(match_id, db_session) -> Match:
    '''Gets Match from database using match_id

    Args:
        match_id ([type]): match id
        db_session ([type]): database session

    Raises:
        ValueError: If no match with match_id is found

    Returns:
        Match: Match with given match_id
    '''
    match = db_session.query(db_models.Match).filter_by(id=match_id).one_or_none()
    if match:
        return Match.from_orm(match)
    raise ValueError(error_messages.MATCH_NOT_FOUND)


def get_matches(filter_dict, db_session) -> List[Match]:
    pass
