"""FET urls."""
from rest_framework.routers import SimpleRouter
from .views import ForeignCurrencyTradesViewSet
from .views import Symbols
from .views import Rate
from django.urls import path
from django.urls import re_path
from django.urls import include
from django.views.decorators.cache import cache_page

router = SimpleRouter()
router.register('fet', ForeignCurrencyTradesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    re_path(
        '^symbols/$',
        cache_page(60 * 60)(Symbols.as_view()),  # cache for save no. of requests to fixer api
        name='api_fixer_symbols'),
    re_path(
        '^rate/$',
        cache_page(60 * 60)(Rate.as_view()),  # cache for save no. of requests to fixer api
        name='api_fixer_symbols'),
]
