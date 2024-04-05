from datetime import datetime
from tortoise.timezone import make_aware


async def make_aware_datetime(start_date: int, end_date: int):
    """
    Convert Unix timestamps to aware datetimes.

    :param start_date: Unix timestamp (milliseconds)
    :param end_date: Unix timestamp (milliseconds)

    :return: A tuple of two aware datetimes
    """
    return (
        make_aware(datetime.fromtimestamp(start_date / 1000)),
        make_aware(datetime.fromtimestamp(end_date / 1000))
    )
