import time

from fastapi import HTTPException

from ..utils.logging import logger
from ..utils.get_params import get_params
from ..models import MerchantTransactionsModel
from ..schemas import MerchantTransactionsSchema


class PerformTransaction:
    """
    PerformTransaction class
    That's used to perform a transaction.

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/metody-merchant-api/performtransaction
    """

    async def __call__(self, params: dict) -> tuple:
        schema = MerchantTransactionsSchema(
            data=get_params(params)
        )
        await schema.is_valid(raise_exception=True)
        clean_data: dict = schema.validated_data
        response: dict = None
        try:
            transaction = await MerchantTransactionsModel.get(_id=clean_data.get("_id"))
            transaction.state = 2
            if transaction.perform_time == 0:
                transaction.perform_time = int(time.time() * 1000)

            await transaction.save()
            response = {
                "result": {
                    "perform_time": int(transaction.perform_time),
                    "transaction": transaction.transaction_id,
                    "state": int(transaction.state),
                }
            }
        except Exception as error:
            logger.error(
                "Error while getting transaction in database: %s", error)
            raise HTTPException(
                status_code=500, detail="Internal server error")

        return transaction.order_id, response
