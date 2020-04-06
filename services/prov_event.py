from sqlalchemy import exc

import db_models
import error_messages
from app_logging import logger
from database import Session
from models import Match, ProviderEvent, Sport


def create_match(match: Match, db_session: Session) -> Match:
    '''Persist match into database.

    Child objects will be created if they dont exist, ignored otherwise

    Args:
        match (Match): Match object
        db_session (Session): Database connection to persist event match

    Returns:
        Match: Updated match data
    '''
    try:
        match_model = db_models.get_match(match, db_session)
        db_session.add(match_model)
        db_session.commit()
    except exc.IntegrityError as ex:
        logger.warning("MATCH: %s ERROR: %s", match, ex)
        raise ValueError(error_messages.DUPLICATE_MATCH)
    return Match.from_orm(match_model)


def update_match_odds(match: Match, db_session: Session) -> Match:
    '''Updates odds of an ongoing match.

    All other changes to existing objects will be ignored

    Args:
        match (Match): Match object
        db_session (Session): Database connection to update the odds

    Returns:
        Match: Updated match data
    '''
    if db_session.query(db_models.Match).filter_by(id=match.id).count() == 0:
        logger.warning("MATCH: %s ERROR: %s", match, error_messages.MATCH_NOT_FOUND)
        raise ValueError(error_messages.MATCH_NOT_FOUND)
    for market in match.markets:
        for selection in market.selections:
            db_session.query(db_models.Selection)\
                .filter(db_models.Selection.id == selection.id)\
                .filter(db_session.query(db_models.match.match_markets_tbl)
                        .filter(db_models.match.match_markets_tbl.c.match_id == match.id)
                        .filter(db_models.match.match_markets_tbl.c.market_id == db_models.Selection.market_id)
                        .exists()
                        )\
                .update({db_models.Selection.odds: selection.odds}, synchronize_session=False)
    db_session.commit()

    return Match.from_orm(db_session.query(db_models.Match).filter_by(id=match.id).one())


def process_event(event: ProviderEvent, db_session: Session) -> ProviderEvent:
    '''Processes incoming events based on event_type

    Args:
        event (ProviderEvent): The incoming event
        db_session (Session): Database connection to persist event match

    Raises:
        ValueError: If even_type is invalid

    Returns:
        ProviderEvent: Event with updated match data
    '''
    if event.message_type == 'UpdateOdds':
        event.event = update_match_odds(event.event, db_session)
        return event
    elif event.message_type == 'NewEvent':
        event.event = create_match(event.event, db_session)
        return event
    else:
        logger.info(
            "EVENT: %s ERROR: %s",
            event,
            error_messages.INVALID_PROVIDEREVENT_MESSAGE_TYPE)
        raise ValueError(error_messages.INVALID_PROVIDEREVENT_MESSAGE_TYPE)
