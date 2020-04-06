import json

import pytest


def test_create_provider_event(test_client, provider_event_new_event):
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
    assert json.loads(response.text)['detail'] == 'message_type must be either UpdateOdds or NewEvent'
