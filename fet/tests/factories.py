"""Factories."""

# Standard Library
from decimal import Decimal

# 3rd-party
import factory

# Local
from ..models import ForeignExchangeTrade


class ForeignExchangeTradeFactory(factory.DjangoModelFactory):

    class Meta:
        model = ForeignExchangeTrade

    sell_currency = factory.faker.Faker('currency_code')
    buy_currency = factory.faker.Faker('currency_code')
    sell_amount = 100.00
    buy_amount = factory.LazyAttribute(lambda o: Decimal(str(round(o.sell_amount * o.rate, 2))))
    rate = 3.789765
