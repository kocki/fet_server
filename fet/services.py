"""Additional bussiness logic implementation."""
import requests
from django.conf import settings
from urllib.parse import urljoin
from decimal import Decimal
from fet.utils import get_payload_data
from decimal import getcontext


class Fixer(object):

    api_url = None
    api_key = None

    def __init__(self):
        """Set up class."""
        self.api_url = getattr(settings, 'FIXER_API_URL', 'http://data.fixer.io/api/')
        self.api_key = getattr(settings, 'FIXER_API_KEY', None)

        if self.api_key is None:
            raise AttributeError('FIXER_API_KEY has to be set in django settings.')

    def _request(self, api_ep, method="GET", params=None, **kwargs):
        """Make a request."""
        if params is None:
            params = {}
        params['access_key'] = self.api_key

        url = urljoin(self.api_url, api_ep)

        response = requests.request(method, url, params=params, **kwargs)
        return get_payload_data(response.content)

    def symbols(self):
        """Returs list of available currency symbols."""
        endpoint = 'symbols'
        data = self._request(endpoint)

        if not data['success']:
            return data

        symbols_list = [*data['symbols']]
        return {
            'currencies': list(zip(symbols_list, symbols_list)),
        }

    def rate(self, sell, buy):
        """Returns rate for selected currency pair."""
        endpoint = 'latest'
        params = {
            'base': sell,
            'symbols': buy,
        }
        data = self._request(endpoint, params=params)

        if not data['success']:
            return data

        # set precision for decimals
        getcontext().prec = 20
        return {
            'rate': Decimal(str(data['rates'][buy])),
        }
