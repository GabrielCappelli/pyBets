''' Glue code between pydantic/sqlalchemy.
    TODO Assuming provider is the system of record and therefore provides valid ids
    TODO adapter/mapper to receive data from multiple providers
'''

from .market import Market
from .match import Match
from .selection import Selection
from .sport import Sport


def get_match(p_model, db_session):
    '''Gets ORM model from Pydantic model'''
    sport = get_sport(p_model.sport, db_session)
    markets = [get_market(m, sport.id, db_session) for m in p_model.markets]
    return Match(
        id=p_model.id,
        url=p_model.url,
        name=p_model.name,
        startTime=p_model.startTime,
        sport=sport,
        markets=markets
    )


def get_sport(p_model, db_session):
    '''Gets ORM model from Pydantic model'''
    sport = db_session.query(Sport).filter_by(id=p_model.id).one_or_none()
    if sport:
        return sport
    return Sport(
        id=p_model.id,
        name=p_model.name
    )


def get_market(p_model, sport_id, db_session):
    '''Gets ORM model from Pydantic model'''
    market = db_session.query(Market).filter_by(id=p_model.id).one_or_none()
    if market:
        return market
    return Market(
        id=p_model.id,
        name=p_model.name,
        sport_id=sport_id,
        selections=[get_selection(s) for s in p_model.selections]
    )


def get_selection(p_model, db_session):
    '''Gets ORM model from Pydantic model'''
    selection = db_session.query(Selection).filter_by(id=p_model.id).one_or_none()
    if selection:
        return selection
    return Selection(
        id=p_model.id,
        name=p_model.name,
        odds=p_model.odds
    )
