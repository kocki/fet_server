"""FET models definition."""

# 3rd-party
from django.db import models
from django.utils.crypto import get_random_string

TRANSACTION_ID_PREFIX = 'TR'
TRANSACTION_ID_LENGTH = 7  # length without prefix


class ForeignExchangeTrade(models.Model):
    """Storage for trades.

    `transaction_id` is intended to use as external unique reference of particular transaction.
    Internally standard Django's integer id field is used for better efficiency.
    """

    transaction_id = models.CharField(
        max_length=9,
        unique=True,
    )
    sell_currency = models.CharField(
        max_length=3,
    )
    sell_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    buy_currency = models.CharField(
        max_length=3,
    )
    buy_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    rate = models.DecimalField(
        max_digits=40,
        decimal_places=20,
    )
    date_booked = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        """Instance identifier."""
        return self.transaction_id

    def save(self, *args, **kwargs):
        """Create transaction id for new instances.

        It is possible to use django signals, if team agree to use it. I prefer to use better
        readable way using predefined model's methods, so I've put it into save().
        """
        if self.pk is None:  # new instance
            self.transaction_id = self.create_transaction_id()

        super(ForeignExchangeTrade, self).save(*args, **kwargs)

    @classmethod
    def create_transaction_id(cls):
        """Create random transaction id."""
        random_part = get_random_string(
            length=TRANSACTION_ID_LENGTH,
            allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
        )
        transaction_id = '{0}{1}'.format(TRANSACTION_ID_PREFIX, random_part)

        if cls.objects.filter(transaction_id=transaction_id).exists():
            return cls.create_transaction_id()

        return transaction_id
