from typing import List

from fastapi import APIRouter, HTTPException

from models import ProviderEvent

provider_router = APIRouter()


@provider_router.post('/', response_model=ProviderEvent)
async def provider_event_route(event: ProviderEvent) -> ProviderEvent:
    '''Creates or updates matches based on incoming events from providers

    Args:
        event (ProviderEvent): Incoming event object

    Returns:
        ProviderEvent: Event with updated Match data if successfull
    '''
    return event
