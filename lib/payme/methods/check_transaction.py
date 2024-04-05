from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from ..utils.logging import logger
from ..models import MerchantTransactionsModel
from ..schemas import MerchantTransactionsSchema as MTS


class CheckTransaction:
    """
    CheckTransaction class
    That's used to check transaction

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/metody-merchant-api/checkperformtransaction
    """

    async def __call__(self, params: dict) -> tuple:
        clean_data: dict = await MTS.get_validated_data(params=params)

        try:
            transaction = await MerchantTransactionsModel.get(_id=clean_data.get("_id"))
            response = {
                "result": {
                    "create_time": int(transaction.created_at_ms),
                    "perform_time": transaction.perform_time,
                    "cancel_time": transaction.cancel_time,
                    "transaction": transaction.transaction_id,
                    "state": transaction.state,
                    "reason": None,
                }
            }
            if transaction.reason is not None:
                response["result"]["reason"] = int(transaction.reason)

        except DoesNotExist:
            logger.error("Transaction does not exist")
            raise HTTPException(
                status_code=404, detail="Transaction does not exist")

        except Exception as e:
            logger.error("Error getting transaction in database: %s", e)
            raise HTTPException(
                status_code=500, detail="Internal server error")

        return None, response
