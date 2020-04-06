import json
from unittest.mock import patch

import pytest
from sqlalchemy import exc

import db_models
import error_messages
from db_models.pydantic_converter import get_market, get_match


def test_provider_event_invalid_message_type(test_client, provider_event_new_event):
    '''
    Given I am a provider
    When I send an event
    And message_type is not in NewEvent, UpdateOdds
    Then I should receive an error message
    '''
    invalid_prov_event = provider_event_new_event
    invalid_prov_event.message_type = 'invalid_msg_type'
    response = test_client.post('/api/provider/', data=invalid_prov_event.json())
    assert response.status_code == 422
    assert json.loads(response.text)['detail'] == error_messages.INVALID_PROVIDEREVENT_MESSAGE_TYPE


@patch('db_models.get_match')
@patch('database.Session')
def test_provider_event_new_event_type(db_mock, get_match_mock, test_client, provider_event_new_event):
    '''
    Given I am a provider
    When I send an event
    And message_type is NewEvent
    Then a new match must be created
    '''
    get_match_mock.return_value = provider_event_new_event.event
    response = test_client.post('/api/provider/', data=provider_event_new_event.json())
    assert response.status_code == 200
    db_mock().add.assert_called_once()
    db_mock().commit.assert_called_once_with()


@patch('db_models.pydantic_converter.get_market')
@patch('db_models.pydantic_converter.get_sport')
def test_provider_event_new_event_market_invalid_sport(get_sport_mock, get_market_mock, provider_event_new_event):
    '''
    Given I am a provider
    When I send an event
    And message_type is NewEvent
    And a market in the message references a sport
    And that market also references a different sport
    Then an error message is displayed
    '''
    get_sport_mock.return_value = db_models.Sport(
        id=0
    )
    get_market_mock.return_value = db_models.Market(
        id=0,
        sport_id=1
    )

    with pytest.raises(ValueError, match=error_messages.INVALID_MARKET_FOR_SPORT):
        get_match(provider_event_new_event.event, None)


@patch('db_models.pydantic_converter.get_selection')
@patch('database.Session')
def test_provider_event_new_event_duplicate_match(db_mock, get_selection_mock):
    '''
    Given I am a provider
    When I send an event
    And message_type is NewEvent
    And a market in the message references a selection
    And that selection also references a different market
    Then an error message is displayed
    '''
    db_session().query().filter_by().one_or_none.return_value = None
    get_selection_mock.return_value = db_models.Selection(
        id=0,
        market_id=1
    )

    with pytest.raises(ValueError, match=error_messages.INVALID_SELECTION_FOR_MARKET):
        get_market(db_models.Market(id=0), None)


@patch('database.Session')
def test_provider_event_new_event_duplicate_match(db_mock, test_client, provider_event_new_event):
    '''
    Given I am a provider
    When I send an event
    And message_type is NewEvent
    And the event Match already exists
    Then an error message is displayed
    '''
    db_mock().commit.side_effect = exc.IntegrityError('mock dupe pk', None, None)
    response = test_client.post('/api/provider/', data=provider_event_new_event.json())
    assert response.status_code == 422
    assert json.loads(response.text)['detail'] == error_messages.INVALID_MARKET_FOR_SPORT


@pytest.mark.skip('TODO')
def test_provider_event_new_event_dont_change_existing_items():
    '''
    Given I am a provider
    When I send an event
    And message_type is NewEvent
    And I reference an existing object (Sport, Market, Selection)
    Then that object is not changed
    '''
    # TODO
    pass


@pytest.mark.skip('TODO')
def test_provider_event_new_event_create_new_items():
    '''
    Given I am a provider
    When I send an event
    And message_type is NewEvent
    And I reference non existing object (Sport, Market, Selection)
    Then that object is created
    '''
    # TODO
    pass


@patch('database.Session')
def test_provider_event_new_event_type(db_mock, test_client, provider_event_update_odds):
    '''
    Given I am a provider
    When I send an event
    And message_type is UpdateOdds
    Then odds for that match are updated
    '''
    db_mock().query().filter_by().count.return_value = 1
    db_mock().query().filter_by().one.return_value = provider_event_update_odds.event
    response = test_client.post('/api/provider/', data=provider_event_update_odds.json())
    assert response.status_code == 200
    db_mock().query()\
        .filter()\
        .filter()\
        .update.assert_called_once_with(
            {
                db_models.Selection.odds: provider_event_update_odds.event.markets[0].selections[0].odds
            }, synchronize_session=False)
    db_mock().commit.assert_called_once_with()


@patch('database.Session')
def test_provider_event_new_event_type_invalid_match_id(db_mock, test_client, provider_event_update_odds):
    '''
    Given I am a provider
    When I send an event
    And message_type is UpdateOdds
    And the Match id is not on the database
    Then an error message is displayed
    '''
    db_mock().query().filter_by().count.return_value = 0
    response = test_client.post('/api/provider/', data=provider_event_update_odds.json())
    assert response.status_code == 422
    assert json.loads(response.text)['detail'] == error_messages.MATCH_NOT_FOUND
