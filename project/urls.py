"""Project URL configuration"""
# 3rd-party
from django.urls import include
from django.urls import path

urlpatterns = [
    path('api/v1/', include('fet.urls')),
]
