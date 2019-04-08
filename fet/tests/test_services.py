"""Tests for services module."""
# Standard Library
from unittest import mock

# 3rd-party
import pytest
from django import test
from django.test import override_settings
from fet.services import Fixer


class TestFixer(test.TestCase):
    """Fixer service tests."""

    @override_settings(FIXER_API_KEY=None)
    def test_no_api_key(self):  # noqa: D102
        with pytest.raises(AttributeError) as exc:
            Fixer()

        assert 'FIXER_API_KEY has to be set in django settings.' in str(exc)

    @mock.patch('fet.services.requests.request')
    def test_request(self, mock_request):  # noqa: D102
        mock_request.return_value.content = b'{}'
        Fixer()._request('test/ep/')

        mock_request.assert_called_once_with(
            'GET',
            'http://data.fixer.io/api/test/ep/',
            params={'access_key': '63d46d3b44fdd339daa9ba25d71ea3e4'},
        )

    @mock.patch('fet.services.Fixer._request')
    def test_symbols(self, mock_request):  # noqa: D102
        mock_request.return_value = {
            'success': True,
            'symbols': {
                'PLN': 'Polish Zloty',
                'GBP': 'British Pound',
            },
        }
        assert Fixer().symbols() == {'symbols': [('PLN', 'PLN'), ('GBP', 'GBP')]}
        mock_request.assert_called_once_with('symbols')

    @mock.patch('fet.services.Fixer._request')
    def test_symbols_failed(self, mock_request):  # noqa: D102
        mock_request.return_value = {
            'success': False,
        }
        assert Fixer().symbols() == mock_request.return_value
        mock_request.assert_called_once_with('symbols')

    @mock.patch('fet.services.Fixer._request')
    def test_rate(self, mock_request):  # noqa: D102
        mock_request.return_value = {
            'success': True,
            "timestamp": 1519296206,
            "base": "USD",
            "date": "2019-04-08",
            "rates": {
                "GBP": 0.72007,
            }
        }

        assert str(Fixer().rate('USD', 'GBP')['rate']) == '0.72007'
        mock_request.assert_called_once_with('latest', params={'base': 'USD', 'symbols': 'GBP'})

    @mock.patch('fet.services.Fixer._request')
    def test_rate_failed(self, mock_request):  # noqa: D102
        mock_request.return_value = {
            'success': False,
        }
        assert Fixer().rate('PLN', 'GBP') == mock_request.return_value
        mock_request.assert_called_once_with('latest', params={'base': 'PLN', 'symbols': 'GBP'})
