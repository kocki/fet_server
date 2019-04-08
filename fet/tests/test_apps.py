# -*- coding: utf-8 -*-
"""Tests for app config module."""

# Django
from django.apps import apps
from django.test import TestCase

# Local
from ..apps import FetConfig


class AppConfigTest(TestCase):  # noqa: D101

    app_name = 'fet'

    def test_apps(self):  # noqa: D102
        assert FetConfig.name == self.app_name
        assert apps.get_app_config(self.app_name).name == self.app_name
