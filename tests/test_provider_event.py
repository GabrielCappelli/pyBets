import json
from unittest.mock import patch

import pytest
from sqlalchemy import exc

import db_models
import error_messages


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
    assert json.loads(response.text)['detail'] == error_messages.DUPLICATE_MATCH


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
