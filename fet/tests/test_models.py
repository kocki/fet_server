"""Models tests."""

# Standard Library
from unittest import mock

# 3rd-party
import pytest
from django import test
from fet.tests.factories import ForeignExchangeTradeFactory


class TestForeignExchangeTrade(test.TestCase):
    """ForeignExchangeTrade tests."""

    def test_str(self):  # noqa: D102
        instance = ForeignExchangeTradeFactory()

        assert str(instance) == instance.transaction_id

    @mock.patch('fet.models.get_random_string')
    def test_repeated_transaction_id(self, mock_get_random_string):  # noqa: D102
        mock_get_random_string.return_value = '1234567'
        ForeignExchangeTradeFactory()
        with pytest.raises(RecursionError):
            ForeignExchangeTradeFactory()
