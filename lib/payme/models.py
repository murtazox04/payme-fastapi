from .utils.logging import logger
from .config import get_settings

from tortoise import fields
from tortoise.models import Model


# Define the MerchantTransactionsModel using Tortoise ORM
class MerchantTransactionsModel(Model):
    """
    MerchantTransactionsModel class
    That's used for managing transactions in database.
    """
    _id = fields.CharField(max_length=255, null=True, blank=False)
    id = fields.BigIntField(pk=True)
    transaction_id = fields.CharField(max_length=255, null=True, blank=False)
    order_id = fields.BigIntField(null=True, blank=True)
    amount = fields.FloatField(null=True, blank=True)
    time = fields.BigIntField(null=True, blank=True)
    perform_time = fields.BigIntField(null=True, default=0)
    cancel_time = fields.BigIntField(null=True, default=0)
    state = fields.IntField(null=True, default=1)
    reason = fields.CharField(max_length=255, null=True, blank=True)
    created_at_ms = fields.CharField(max_length=255, null=True, blank=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return str(self._id)

    class Meta:
        table = "merchant_transactions"  # Define the table name explicitly


class Order(Model):
    """
    Order class \
        That's used for managing order process
    """
    id = fields.BigIntField(pk=True)
    amount = fields.IntField(null=True, blank=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self) -> str:
        return f"ORDER ID: {self.pk} - AMOUNT: {self.amount}"

    class Meta:
        managed = False
        table = "orders"


async def get_order_model():
    """
    Retrieves the Order model, either the custom model or the default one.
    """
    settings = get_settings

    try:
        CUSTOM_ORDER = settings.payme.order_model

        if isinstance(CUSTOM_ORDER, Model):
            return CUSTOM_ORDER
        else:
            raise TypeError(
                "The input must be an instance of tortoise.models.Model")
    except (ImportError, AttributeError):
        logger.warning("You have no payme custom order model")
        CUSTOM_ORDER = None

        return Order
