import json


async def to_json(**kwargs) -> dict:
    """
    Use this async method to data dumps.
    """
    data: dict = {
        "method": kwargs.pop("method"),
        "params": kwargs.pop("params"),
    }

    return json.dumps(data)
