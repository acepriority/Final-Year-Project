from django.urls import path
from trader_app.views import Trader, ViewLicense, ViewPermit, TraderProfile

urlpatterns = [
    path('trader/', Trader.as_view(), name='trader'),
    path('license/', ViewLicense.as_view(), name='license'),
    path('permit/<int:permitId>/', ViewPermit.as_view(), name='permit'),
    path('trader_profile/', TraderProfile.as_view(), name='trader_profile')
]
