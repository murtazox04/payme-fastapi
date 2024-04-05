from fastapi import HTTPException


class BasePaymeException(HTTPException):
    """
    BasePaymeException is a custom exception class for Payme API.
    """

    def __init__(self, status_code: int = 200, error_code: int = None, message: dict = None):
        detail = {
            "error": {
                "code": error_code,
                "message": message
            }
        }
        super().__init__(status_code=status_code, detail=detail)


class PermissionDenied(BasePaymeException):
    """
    PermissionDenied is raised when the client is not allowed to access the server.
    """

    def __init__(self):
        message = {
            "uz": "Ruxsat berilmagan",
            "ru": "Доступ запрещен",
            "en": "Permission denied"
        }
        super().__init__(status_code=403, error_code=-32504, message=message)


class MethodNotFound(BasePaymeException):
    """
    MethodNotFound is raised when the requested method does not exist.
    """

    def __init__(self):
        message = {
            "uz": "Metod topilmadi",
            "ru": "Метод не найден",
            "en": "Method not found"
        }
        super().__init__(status_code=405, error_code=-32601, message=message)


class TooManyRequests(BasePaymeException):
    """
    TooManyRequests is raised when the request exceeds the limit.
    """

    def __init__(self):
        message = {
            "uz": "Buyurtma tolovni amalga oshirish jarayonida",
            "ru": "Транзакция в очереди",
            "en": "Order payment status is queued"
        }
        super().__init__(status_code=429, error_code=-31099, message=message)


class IncorrectAmount(BasePaymeException):
    """
    IncorrectAmount is raised when the amount is incorrect.
    """

    def __init__(self):
        message = {
            'ru': 'Неверная сумма',
            'uz': "Noto'g'ri qiymat",
            'en': 'Incorrect amount',
        }
        super().__init__(status_code=400, error_code=-31001, message=message)


class PerformTransactionDoesNotExist(BasePaymeException):
    """
    PerformTransactionDoesNotExist is raised when a transaction does not exist or deleted.
    """

    def __init__(self):
        message = {
            "uz": "Buyurtma topilmadi",
            "ru": "Заказ не существует",
            "en": "Order does not exist"
        }
        super().__init__(status_code=404, error_code=-31050, message=message)


class PaymeTimeoutException(Exception):
    """
    PaymeTimeoutException is raised when Payme is working slowly.
    """
    pass
