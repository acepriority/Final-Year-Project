from django.urls import path
from trader_app.views import (
    Trader,
    ViewPermit,
    TraderProfile,
    MakePermitRequest)

urlpatterns = [
    path('trader/', Trader.as_view(), name='trader'),
    path('permit/<int:permitId>/', ViewPermit.as_view(), name='permit'),
    path('trader_profile/', TraderProfile.as_view(), name='trader_profile'),
    path('permit_request/', MakePermitRequest.as_view(), name='permit_request')
]
