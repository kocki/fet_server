"""Additional tools for app."""
import json


def get_payload_data(payload, json_fallback=True):
    """Return JSON payload data as a dictionary."""
    try:
        data = json.loads(payload.decode('utf-8'))
    except Exception as exc:
        if json_fallback:
            data = {'error': repr(exc), 'payload': payload}
        else:
            raise exc
    return data


def get_list_from_choices(choices, idx=0):
    """Return list of data extracted from choices list.

    :param choices: list of two-element tuples
    :param idx: which element of tuple would be return in list
    :returns: list of selected elements
    """
    return list(zip(*choices))[idx]
