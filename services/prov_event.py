import error_messages
from models import ProviderEvent


def process_event(event: ProviderEvent) -> ProviderEvent:
    if event.message_type == 'UpdateOdds':
        pass
    elif event.message_type == 'NewEvent':
        pass
    else:
        raise ValueError(error_messages.INVALID_PROVIDEREVENT_MESSAGE_TYPE)
