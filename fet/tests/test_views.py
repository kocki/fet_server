# Standard Library
from decimal import Decimal
from decimal import getcontext

# 3rd-party
from django.urls import reverse
from fet.tests.factories import ForeignExchangeTradeFactory
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from ..models import ForeignExchangeTrade
from unittest import mock


class TestForeignExchangeTradesViewSet(APITestCase):
    """ForeignExchangeTradesViewSet tests."""

    def setUp(self):  # noqa: D102
        self.client = APIClient()

    def test_foreign_exchange_trade_viewset(self):  # noqa: D102
        trade_instance = ForeignExchangeTradeFactory()
        trade_instance.refresh_from_db()

        base_url = reverse('foreignexchangetrade-list')
        response = self.client.get(base_url)
        data = response.data

        assert data['count'] == 1

        trade = data['results'][0]
        assert trade['sell_currency'] == trade_instance.sell_currency
        assert trade['buy_currency'] == trade_instance.buy_currency

        getcontext().prec = 2
        assert Decimal(trade['sell_amount']) == trade_instance.sell_amount
        assert Decimal(trade['buy_amount']) == trade_instance.buy_amount

        getcontext().prec = 20
        assert Decimal(trade['rate']) == trade_instance.rate
        assert trade['date_booked'] == trade_instance.date_booked.isoformat()
        assert trade['transaction_id'] == trade_instance.transaction_id

    @mock.patch('fet.serializers.get_list_from_choices')
    @mock.patch('fet.serializers.Fixer')
    def test_foreign_exchange_trade_viewset_create(self, mock_fixer, mock_symbols):  # noqa: D102
        mock_symbols.return_value = ['PLN', 'GBP']
        getcontext().prec = 2
        mock_fixer.return_value.rate.return_value = {'rate': Decimal('4.9991')}

        base_url = reverse('foreignexchangetrade-list')
        data = {
            'sell_currency': 'GBP',
            'buy_currency': 'PLN',
            'sell_amount': 1000,
            'rate': 4.9991,

        }
        response = self.client.post(base_url, data)
        data = response.data
        new_trade = ForeignExchangeTrade.objects.first()

        assert ForeignExchangeTrade.objects.count() == 1
        assert data['transaction_id'] == new_trade.transaction_id
        assert str(data['buy_amount']) == str(new_trade.buy_amount)


class TestFixerView(APITestCase):
    """FixerView tests."""

    def setUp(self):  # noqa: D102
        self.client = APIClient()

    @mock.patch('fet.views.Fixer')
    def test_rate(self, mock_fixer):  # noqa: D102
        mock_fixer.return_value.rate.return_value = {'rate': Decimal('4.9991')}
        base_url = reverse('api-fixer-rate')
        params = {
            'sell': 'GBP',
            'buy': 'PLN',
        }
        print(self.client.get(base_url, params).content)
        print(mock_fixer.__dict__)

        assert mock_fixer.call_count == 1

