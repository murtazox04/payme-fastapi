from fastapi import HTTPException

from ..utils.logging import logger
from ..models import MerchantTransactionsModel
from ..utils.make_aware_datetime import make_aware_datetime as mad
from ..schemas import MerchantTransactionsSchema as MTS


class GetStatement:
    """
    GetStatement class
    Transaction information is used for reconciliation
    of merchant and Payme Business transactions.

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/metody-merchant-api/getstatement
    """

    async def __call__(self, params: dict) -> tuple:
        clean_data: dict = await MTS.get_validated_data(params=params)

        start_date, end_date = mad(
            int(clean_data.get("start_date")),
            int(clean_data.get("end_date"))
        )

        try:
            transactions = await MerchantTransactionsModel.filter(
                created_at__gte=start_date,
                created_at__lte=end_date
            )

            if not transactions:  # no transactions found for the period
                return None, {"result": {"transactions": []}}

            statements = [
                {
                    'id': t._id,
                    'time': int(t.created_at.timestamp()),
                    'amount': t.amount,
                    'account': {'order_id': t.order_id},
                    'create_time': int(t.created_at_ms),
                    'perform_time': t.perform_time,
                    'cancel_time': t.cancel_time,
                    'transaction': t.order_id,
                    'state': t.state,
                    'reason': int(t.reason) if t.reason is not None else None,
                    'receivers': []  # not implemented
                } for t in transactions
            ]

            response: dict = {
                "result": {
                    "transactions": statements
                }
            }
        except Exception as error:
            logger.error("Error getting transaction in database: %s", error)
            raise HTTPException(
                status_code=500, detail="Internal server error")

        return None, response
