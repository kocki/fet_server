"""REST API serializers."""
from rest_framework import serializers

from fet.services import Fixer
from django.core.cache import cache

from fet.utils import get_list_from_choices
from .models import ForeignCurrencyTrades
from rest_framework import exceptions


class ForeignCurrencyTradesSerializer(serializers.ModelSerializer):
    """Serializer for ForeignCurrencyTrades data."""

    transaction_id = serializers.CharField(required=False)
    buy_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    date_booked = serializers.DateTimeField(required=False)

    class Meta:
        model = ForeignCurrencyTrades
        fields = (
            'transaction_id',
            'sell_currency',
            'sell_amount',
            'buy_currency',
            'buy_amount',
            'rate',
            'date_booked',
        )

    @staticmethod
    def validate_rate_data(rate_data, sell_currency, rate):
        """Check last rate for errors and compare with payload."""
        if 'error' in rate_data:
            if rate_data['error']['type'] == 'base_currency_access_restricted':
                detail = 'Sell currency access restricted ({0}).'.format(sell_currency)
            else:
                detail = 'Unrecognized error code: {0}'.format(rate_data['error']['code'])

            raise exceptions.ValidationError(
                code=rate_data['error']['type'],
                detail=detail,
            )

        if rate_data['rate'] != rate:
            # below error would provide to refresh data on frontend (cache is flushed)
            cache.clear()
            raise exceptions.ValidationError(
                code='currency_rate_error',
                detail="Currency rate error.",
            )

        return rate_data['rate']

    def validate(self, data):
        """Check is rate same like current one.

        We have to protect our transaction for hacks:
        - passing wrong rates via api: we check payload rate with current one
        - preparing transaction with period before accepting (paying it)
        """
        fixer = Fixer()
        symbols = get_list_from_choices(fixer.symbols()['symbols'])
        sell_currency = data['sell_currency']
        buy_currency = data['buy_currency']
        rate = data['rate']

        symbols_check = {sell_currency, buy_currency}.difference(symbols)
        if symbols_check:
            raise exceptions.ValidationError(
                code='disallowed_currency_symbol',
                detail='{0}'.format(', '.join(symbols_check)),
            )

        self.validate_rate_data(
            fixer.rate(sell_currency, buy_currency),
            sell_currency,
            rate,
        )

        data['buy_amount'] = data['sell_amount'] * rate
        return data
