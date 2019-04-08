"""Utils tests."""

# 3rd-party
import pytest
# Django
from django.test import TestCase

# Local
from ..utils import get_list_from_choices
from ..utils import get_payload_data


class TestUtils(TestCase):
    """Tests for utils module."""

    def setUp(self):  # noqa: D102
        self.json_content = {
            'some': 'json',
            'data': '{{with_template.tag}}',
            'and': 999,
        }

    def test_get_payload_data_json_error(self):  # noqa: D102
        data = None

        assert get_payload_data(data)['payload'] == data

    def test_get_payload_data_raise_error(self):  # noqa: D102
        data = 'Any string'
        with pytest.raises(AttributeError):
            assert get_payload_data(data, json_fallback=False)

    def test_get_list_from_choices(self):  # noqa: D102
        data = [
            (1, 'one'),
            (2, 'two'),
            (3, 'three'),
        ]
        assert list(get_list_from_choices(data)) == [1, 2, 3]
        assert list(get_list_from_choices(data, 1)) == ['one', 'two', 'three']
