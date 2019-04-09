"""REST API serializers."""

# 3rd-party
from fet.services import Fixer
from fet.utils import get_list_from_choices
from rest_framework import exceptions
from rest_framework import serializers

# Local
from .models import ForeignExchangeTrade


class ForeignExchangeTradeSerializer(serializers.ModelSerializer):
    """Serializer for ForeignExchangeTrade data."""

    transaction_id = serializers.CharField(required=False)
    buy_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    rate = serializers.DecimalField(max_digits=40, decimal_places=20, required=False)
    date_booked = serializers.SerializerMethodField(required=False)

    class Meta:
        model = ForeignExchangeTrade
        fields = (
            'transaction_id',
            'sell_currency',
            'sell_amount',
            'buy_currency',
            'buy_amount',
            'rate',
            'date_booked',
        )

    def get_date_booked(self, obj):
        """Return properly formatted time."""
        return obj.date_booked.isoformat()

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
                detail='Disallowed currency symbol: {0}'.format(', '.join(symbols_check)),
            )

        self.validate_rate_data(
            fixer.rate(sell_currency, buy_currency),
            sell_currency,
            rate,
        )

        data['buy_amount'] = data['sell_amount'] * rate
        return data
