from models import ProviderEvent


def process_event(event: ProviderEvent) -> ProviderEvent:
    if event.message_type == 'UpdateOdds':
        pass
    elif event.message_type == 'NewEvent':
        pass
    else:
        raise ValueError('message_type must be either UpdateOdds or NewEvent')
