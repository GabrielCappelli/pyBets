import json
from unittest.mock import patch

import pytest
from sqlalchemy import exc

import db_models
import error_messages
from db_models.pydantic_converter import get_market, get_match


@patch('database.Session')
def test_get_match(db_mock, test_client, valid_match):
    '''
    Given I am a user
    When I request a match
    And I pass a valid match id
    Then I should receive match details
    '''
    db_mock().query().filter_by().one_or_none.return_value = valid_match
    response = test_client.get('/api/match/0')
    assert response.status_code == 200
    assert json.loads(response.text)['id'] == valid_match.id


@patch('database.Session')
def test_get_match_invalid_id(db_mock, test_client, valid_match):
    '''
    Given I am a user
    When I request a match
    And I pass an invalid match id
    Then I should receive an error
    '''
    db_mock().query().filter_by().one_or_none.return_value = None
    response = test_client.get('/api/match/0')
    assert response.status_code == 422
    assert json.loads(response.text)['detail'] == error_messages.MATCH_NOT_FOUND
