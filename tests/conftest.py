from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from application import create_app
from models import Market, Match, ProviderEvent, Selection, Sport


@pytest.fixture
def test_client() -> TestClient:
    '''Fixture to creaete a FastAPI TestClient'''
    app = create_app()
    return TestClient(app)


@pytest.fixture
def provider_event_new_event(valid_match) -> ProviderEvent:
    '''Fixture to create a ProviderEvent with type NewEvent'''
    return ProviderEvent(
        id=0,
        message_type='NewEvent',
        event=valid_match
    )


@pytest.fixture
def valid_match(valid_sport, valid_market) -> Match:
    '''Fixture to create a valid Match'''
    return Match(
        id=0,
        url='/api/match/0',
        name='Test Match',
        startTime=datetime.utcnow(),
        sport=valid_sport,
        markets=[valid_market]
    )


@pytest.fixture
def valid_sport() -> Sport:
    return Sport(
        id=0,
        name='Test Sport'
    )


@pytest.fixture
def valid_market(valid_selection) -> Market:
    return Market(
        id=0,
        name='Winner',
        selections=[valid_selection]
    )


@pytest.fixture
def valid_selection() -> Selection:
    return Selection(
        id=0,
        name='Test Team',
        odds=1.0
    )
