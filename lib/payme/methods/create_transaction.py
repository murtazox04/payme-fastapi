import uuid
import time
import datetime

from fastapi import HTTPException
from ..utils.logging import logger
from ..utils.get_params import get_params
from ..models import MerchantTransactionsModel
from ..errors.exceptions import TooManyRequests
from ..schemas import MerchantTransactionsSchema


class CreateTransaction:
    """
    CreateTransaction class
    That's used to create transaction

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/metody-merchant-api/createtransaction
    """

    async def __call__(self, params: dict) -> tuple:
        schema = MerchantTransactionsSchema(
            data=await get_params(params)
        )
        await schema.is_valid(raise_exception=True)
        order_id = schema.validated_data.get("order_id")

        try:
            transaction = await MerchantTransactionsModel.filter(order_id=order_id).last()

            if transaction is not None:
                if transaction._id != schema.validated_data.get("_id"):
                    raise TooManyRequests()

        except TooManyRequests as error:
            logger.error("Too many requests for transaction %s", error)
            raise HTTPException(
                status_code=429, detail="Too many requests") from error

        if transaction is None:
            transaction = await MerchantTransactionsModel.create(
                _id=schema.validated_data.get('_id'),
                order_id=schema.validated_data.get('order_id'),
                transaction_id=uuid.uuid4(),
                amount=schema.validated_data.get('amount'),
                created_at_ms=int(time.time() * 1000),
            )

        response: dict = {
            "result": {
                "create_time": int(transaction.created_at_ms),
                "transaction": transaction.transaction_id,
                "state": int(transaction.state),
            }
        }

        return order_id, response

    @staticmethod
    async def _convert_ms_to_datetime(time_ms: int) -> datetime:
        """Use this format to convert from time ms to datetime format.
        """
        readable_datetime = datetime.datetime.fromtimestamp(time_ms / 1000)

        return readable_datetime
