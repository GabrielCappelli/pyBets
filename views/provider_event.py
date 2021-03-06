from typing import List

from fastapi import APIRouter, Depends, HTTPException

from database import Session, get_request_session
from models import ProviderEvent
from services.prov_event import process_event

provider_router = APIRouter()


@provider_router.post('/', response_model=ProviderEvent)
async def provider_event_route(event: ProviderEvent, db_session: Session = Depends(get_request_session)) -> ProviderEvent:
    '''Creates or updates matches based on incoming events from providers

    Args:
        event (ProviderEvent): Incoming event object

    Returns:
        ProviderEvent: Event with updated Match data if successfull
    '''
    try:
        return process_event(event, db_session)
    except ValueError as ex:
        raise HTTPException(422, str(ex))
    except Exception as ex:
        raise HTTPException(500, str(ex))
