import base64
from decimal import Decimal
from dataclasses import dataclass
from typing import Optional

from config import get_settings


settings = get_settings()
PAYME_ID = settings.payme.id
PAYME_ACCOUNT = settings.payme.account
PAYME_CALL_BACK_URL = settings.payme.call_back_url
PAYME_URL = settings.payme.url


@dataclass
class GeneratePayLink:
    """
    GeneratePayLink dataclass
    That's used to generate pay link for each order.

    Parameters
    ----------
    order_id: str — The order_id for paying
    amount: Decimal — The amount belong to the order
    callback_url: str \
        The merchant api callback url to redirect after payment. Optional parameter.
        By default, it takes PAYME_CALL_BACK_URL from your settings

    Returns str — pay link
    ----------------------

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/initsializatsiya-platezhey/
    """
    order_id: str
    amount: Decimal
    callback_url: Optional[str] = None

    async def generate_link(self) -> str:
        """
        GeneratePayLink for each order.
        """
        redirect_url = self.callback_url or PAYME_CALL_BACK_URL

        params = f'm={PAYME_ID};ac.{PAYME_ACCOUNT}={self.order_id};a={self.amount};c={redirect_url}'
        encoded_params = base64.b64encode(
            params.encode('utf-8')).decode('utf-8')

        return f"{PAYME_URL}/{encoded_params}"

    @staticmethod
    async def to_tiyin(amount: Decimal) -> Decimal:
        """
        Convert from sum to tiyin.

        Parameters
        ----------
        amount: Decimal -> order amount
        """
        return amount * 100

    @staticmethod
    async def to_sum(amount: Decimal) -> Decimal:
        """
        Convert from tiyin to sum.

        Parameters
        ----------
        amount: Decimal -> order amount
        """
        return amount / 100
