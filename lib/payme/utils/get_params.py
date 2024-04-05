from tortoise import Tortoise
from tortoise.exceptions import ConfigurationError


async def get_params(params: dict) -> dict:
    """
    Use this function to get the parameters from the payme.
    """
    account = params.get("account")

    clean_params = {}
    clean_params["_id"] = params.get("id")
    clean_params["time"] = params.get("time")
    clean_params["amount"] = params.get("amount")
    clean_params["reason"] = params.get("reason")

    # get statement method params
    clean_params["start_date"] = params.get("from")
    clean_params["end_date"] = params.get("to")

    if account is not None:
        account_name = Tortoise.get_connection(
            "default").config_dict.get("PAYME_ACCOUNT")
        if not account_name:
            raise ConfigurationError(
                "PAYME_ACCOUNT not found in database configuration")
        clean_params["order_id"] = account.get(account_name)

    return clean_params
