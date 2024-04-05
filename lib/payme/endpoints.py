import base64
import binascii

from pydantic import ValidationError
from fastapi.responses import Response
from fastapi import APIRouter, HTTPException, Request

from .config import get_settings
from .methods.get_statement import GetStatement
from .methods.check_transaction import CheckTransaction
from .methods.cancel_transaction import CancelTransaction
from .methods.create_transaction import CreateTransaction
from .methods.perform_transaction import PerformTransaction
from .methods.check_perform_transaction import CheckPerformTransaction
from .errors.exceptions import MethodNotFound, PermissionDenied, PerformTransactionDoesNotExist
from .utils.logging import logger


router = APIRouter()


@router.post("/merchant/")
async def merchant_api(request: Request) -> Response:
    """
    MerchantAPIView class provides payme call back functionality.
    """
    password = request.get('authorization')
    if not authorize(password):
        raise HTTPException(status_code=401, detail="Unauthorized")

    incoming_method = request.get("method")
    logger.info("Call back data is incoming %s", request)

    try:
        paycom_method = get_paycom_method_by_name(incoming_method)
    except (MethodNotFound, ValidationError, PerformTransactionDoesNotExist) as error:
        logger.error(f"Error occurred: {error}")
        raise HTTPException(status_code=400, detail=str(error))

    order_id, action = await paycom_method(request.get("params"))

    if isinstance(paycom_method, CreateTransaction):
        await create_transaction(order_id, action)

    if isinstance(paycom_method, PerformTransaction):
        await perform_transaction(order_id, action)

    if isinstance(paycom_method, CancelTransaction):
        await cancel_transaction(order_id, action)

    return Response(content=action)


async def get_paycom_method_by_name(incoming_method: str):
    """
    Use this static method to get the paycom method by name.
    :param incoming_method: string -> incoming method name
    """
    available_methods = {
        "CheckPerformTransaction": CheckPerformTransaction,
        "CreateTransaction": CreateTransaction,
        "PerformTransaction": PerformTransaction,
        "CancelTransaction": CancelTransaction,
        "CheckTransaction": CheckTransaction,
        "GetStatement": GetStatement
    }

    try:
        merchant_method = available_methods[incoming_method]()
    except KeyError:
        error_message = f"Unavailable method: {incoming_method}"
        logger.error(error_message)
        raise MethodNotFound(error_message=error_message)

    return merchant_method


async def authorize(password: str) -> bool:
    """
    Authorize the Merchant.
    :param password: string -> Merchant authorization password
    """
    is_payme = False

    if not isinstance(password, str):
        logger.error("Request from an unauthorized source!")
        raise PermissionDenied(
            error_message="Request from an unauthorized source!")

    password = password.split()[-1]

    try:
        password = base64.b64decode(password).decode('utf-8')
    except (binascii.Error, UnicodeDecodeError) as error:
        logger.error("Error when authorize request to merchant!")
        raise PermissionDenied(
            error_message="Error when authorize request to merchant!") from error

    merchant_key = password.split(':')[-1]
    settings = get_settings()
    if merchant_key == settings.payme.key:
        is_payme = True

    if merchant_key != settings.payme.key:
        logger.error("Invalid key in request!")

    if not is_payme:
        raise PermissionDenied(
            error_message="Unavailable data for unauthorized users!")

    return is_payme


async def create_transaction(order_id, action) -> None:
    """
    need implement in your view class
    """
    pass


async def perform_transaction(order_id, action) -> None:
    """
    need implement in your view class
    """
    pass


async def cancel_transaction(order_id, action) -> None:
    """
    need implement in your view class
    """
    pass
