"""REST API views for FET."""

# 3rd-party
from django.http import JsonResponse
from rest_framework import exceptions
from rest_framework import mixins
from rest_framework import views
from rest_framework import viewsets

# Local
from .models import ForeignExchangeTrade
from .serializers import ForeignExchangeTradeSerializer
from .services import Fixer


class ForeignExchangeTradesViewSet(mixins.ListModelMixin,
                                   mixins.CreateModelMixin,
                                   viewsets.GenericViewSet):
    """REST API view for list and create instances of ForeignExchangeTrade."""

    queryset = ForeignExchangeTrade.objects.all().order_by('-date_booked')
    serializer_class = ForeignExchangeTradeSerializer


class FixerView(views.APIView):
    """Base quotation API view."""

    api = Fixer()
    method = None

    def get(self, request, *args, **kwargs):
        """Change choices to JSON."""
        return JsonResponse(getattr(self.api, self.method)(*args))


class SymbolsView(FixerView):
    """Address Choices for selected post code."""

    method = 'symbols'


class RateView(FixerView):
    """Address Choices for selected post code.

    Query params:
    :param sell: source currency
    :param buy: destination currency
    """

    method = 'rate'

    def get(self, request, *args, **kwargs):
        sell = request.GET.get('sell')
        buy = request.GET.get('buy')
        if sell and buy:
            return super(RateView, self).get(request, sell, buy, *args, **kwargs)
        raise exceptions.ValidationError(
            detail='Query params `sell` and `buy` must be set.',
            code='query_params_error',
        )
