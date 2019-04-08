"""Serializers tests."""
import pytest

from ..serializers import ForeignExchangeTradeSerializer
from django import test
from rest_framework import exceptions


class TestForeignExchangeTradeSerializer(test.TestCase):
    """ForeignExchangeTradeSerializer tests."""

    def setUp(self):  # noqa: D102
        self.serializer = ForeignExchangeTradeSerializer()

    def test_validate_rate_base_error_wrong_rate(self):  # noqa: D102
        rate_data = {'rate': 4.9991}
        sell_currency = 'GBP'
        rate = 4.99912

        with pytest.raises(exceptions.ValidationError) as exc:
            self.serializer.validate_rate_data(rate_data, sell_currency, rate)

        assert 'currency_rate_error' in str(exc)

    def test_validate_rate_base_error_currency_access_restricted(self):  # noqa: D102
        rate_data = {'error': {'type': 'base_currency_access_restricted'}}
        sell_currency = 'GBP'
        rate = 4.9991

        with pytest.raises(exceptions.ValidationError) as exc:
            self.serializer.validate_rate_data(rate_data, sell_currency, rate)

        assert rate_data['error']['type'] in str(exc)

    def test_validate_rate_base_error_other(self):  # noqa: D102
        rate_data = {'error': {'type': 'other_error', 'code': 123}}
        sell_currency = 'GBP'
        rate = 4.9991

        with pytest.raises(exceptions.ValidationError) as exc:
            self.serializer.validate_rate_data(rate_data, sell_currency, rate)

        assert rate_data['error']['type'] in str(exc)
