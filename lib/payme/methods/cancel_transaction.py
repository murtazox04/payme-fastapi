import time
from typing import Tuple

from fastapi import HTTPException
from tortoise.transactions import atomic

from ..utils.logging import logger
from ..models import MerchantTransactionsModel
from ..errors.exceptions import PerformTransactionDoesNotExist
from ..schemas import MerchantTransactionsSchema as MTS


class CancelTransaction:
    """
    CancelTransaction class
    That is used to cancel a transaction.

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/metody-merchant-api/canceltransaction
    """

    async def __call__(self, params: dict) -> Tuple[str, dict]:
        clean_data: dict = MTS.get_validated_data(params=params)

        try:
            async with atomic():
                transactions: MerchantTransactionsModel = await MerchantTransactionsModel.filter(
                    _id=clean_data.get('_id')
                ).first()
                if transactions.cancel_time == 0:
                    transactions.cancel_time = int(time.time() * 1000)
                if transactions.perform_time == 0:
                    transactions.state = -1
                if transactions.perform_time != 0:
                    transactions.state = -2
                transactions.reason = clean_data.get("reason")
                await transactions.save()

        except PerformTransactionDoesNotExist as error:
            logger.error("Paycom transaction does not exist: %s", error)
            raise HTTPException(
                status_code=404, detail="Transaction does not exist")

        response: dict = {
            "result": {
                "state": transactions.state,
                "cancel_time": transactions.cancel_time,
                "transaction": transactions.transaction_id,
                "reason": int(transactions.reason),
            }
        }

        return transactions.order_id, response
