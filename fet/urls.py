"""FET urls."""
# 3rd-party
from django.urls import include
from django.urls import path
from django.urls import re_path
from rest_framework.routers import SimpleRouter

# Local
from .views import ForeignExchangeTradesViewSet
from .views import RateView
from .views import SymbolsView

router = SimpleRouter()
router.register('fet', ForeignExchangeTradesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    re_path(
        '^symbols/$',
        SymbolsView.as_view(),  # cache for save no. of requests to fixer api
        name='api-fixer-symbols'),
    re_path(
        '^rate/$',
        RateView.as_view(),  # cache for save no. of requests to fixer api
        name='api-fixer-rate'),
]
