from ..utils.get_params import get_params
from ..schemas import MerchantTransactionsSchema


class CheckPerformTransaction:
    """
    CheckPerformTransaction class
    That's used to check perform transaction.

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/metody-merchant-api/checktransaction
    """

    async def __call__(self, params: dict) -> tuple:
        schema = MerchantTransactionsSchema(
            data=await get_params(params)
        )
        await schema.is_valid(raise_exception=True)

        response = {
            "result": {
                "allow": True,
            }
        }

        return None, response
