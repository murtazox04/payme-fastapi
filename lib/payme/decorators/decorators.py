import functools
from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientResponseError

from ..utils.logging import logger
from ..errors.exceptions import PaymeTimeoutException


def payme_request(func):
    """
    Payme request decorator.
    """
    @functools.wraps(func)
    async def wrapper(self, data):
        response = None
        req_data = {
            "method": "POST",
            "url": self.base_url,
            "data": data,
            "headers": self.headers,
        }
        timeout = ClientTimeout(total=self.timeout)
        async with ClientSession(timeout=timeout) as session:
            try:
                async with session.request(**req_data) as resp:
                    resp.raise_for_status()
                    response = await resp.json()
            except ClientResponseError as error:
                logger.info("Payme request has failed with error: %s", error)
                raise PaymeTimeoutException(
                    f"Payme request failed: {error.status} {error.message}") from error
            except Exception as e:
                logger.exception("An error occurred during Payme request")
                raise PaymeTimeoutException(
                    "An error occurred during Payme request") from e
        return response

    return wrapper
