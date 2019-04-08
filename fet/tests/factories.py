"""Factories."""

# 3rd-party
import factory
from factory import fuzzy

# Local
from ..models import ForeignExchangeTrade


class ForeignExchangeTradeFactory(factory.DjangoModelFactory):

    class Meta:
        model = ForeignExchangeTrade

    sell_currency = factory.faker.Faker('currency_code')
    buy_currency = factory.faker.Faker('currency_code')
    sell_amount = fuzzy.FuzzyDecimal(1, 999999.99, precision=2)
    buy_amount = factory.LazyAttribute(lambda o: round(o.sell_amount * o.rate, 2))
    rate = fuzzy.FuzzyDecimal(0.000001, 999.999999, precision=20)
