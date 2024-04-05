from typing import Optional

from pydantic import BaseModel, validator

from .models import Order
from .config import get_settings
from .errors.exceptions import IncorrectAmount, PerformTransactionDoesNotExist
from .utils.get_params import get_params
from .utils.logging import logger


class MerchantTransactionsSchema(BaseModel):
    """
    MerchantTransactionsModelSerializer class
    That's used to serialize merchant transactions data.
    """
    _id: Optional[str]
    transaction_id: Optional[str]
    order_id: Optional[int]
    amount: Optional[float]
    time: Optional[int]
    perform_time: Optional[int]
    cancel_time: Optional[int]
    state: Optional[int]
    reason: Optional[str]
    created_at_ms: Optional[str]
    start_date: Optional[int]
    end_date: Optional[int]

    @validator('amount', pre=True)  # Prioritize to catch errors early
    def validate_amount(cls, value: Optional[float]) -> float:
        """
        Validator for Transactions Amount.
        """
        settings = get_settings()
        if value is not None and value <= settings.payme.min_amount:
            raise IncorrectAmount("Payment amount is less than allowed.")
        return value

    @validator('order_id')
    def validate_order_id(cls, value: int) -> int:
        """
        Use this method to check if a transaction is allowed to be executed.

        Parameters
        ----------
        value: int -> Order ID.
        """
        if not Order.filter(id=value).exists():
            logger.error("Order does not exist order_id: %s", value)
            raise PerformTransactionDoesNotExist()
        return value

    @classmethod
    def get_validated_data(cls, params: dict) -> dict:
        """
        This static method helps to get validated data.

        Parameters
        ----------
        params: dict — Includes request params.
        """
        clean_data = get_params(params)
        return cls(**clean_data).dict()
