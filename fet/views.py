"""REST API views for FET."""
from django.http import JsonResponse
from rest_framework import mixins
from rest_framework import views
from rest_framework import viewsets
from rest_framework import exceptions
from .models import ForeignCurrencyTrades
from .serialiers import ForeignCurrencyTradesSerializer
from .services import Fixer


class ForeignCurrencyTradesViewSet(mixins.ListModelMixin,
                                   mixins.CreateModelMixin,
                                   viewsets.GenericViewSet):
    """REST API view for list and create instances of ForeignCurrencyTrades."""

    queryset = ForeignCurrencyTrades.objects.all().order_by('-date_booked')
    serializer_class = ForeignCurrencyTradesSerializer

    def create(self, request, *args, **kwargs):

        return super(ForeignCurrencyTradesViewSet, self).create(request, *args, **kwargs)


class FixerView(views.APIView):
    """Base quotation API view."""

    api = Fixer()
    method = None

    def get(self, request, *args, **kwargs):
        """Change choices to JSON."""
        return JsonResponse(getattr(self.api, self.method)(*args))


class Symbols(FixerView):
    """Address Choices for selected post code."""

    method = 'symbols'


class Rate(FixerView):
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
            return super(Rate, self).get(request, sell, buy, *args, **kwargs)
        raise exceptions.ValidationError(
            detail='Query params `sell` and `buy` must be set.',
            code='query_params_error',
        )
