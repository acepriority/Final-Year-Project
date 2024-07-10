from django.urls import path
from trader_app.views import (
    Trader,
    ViewPermit,
    TraderProfile,
    MakePermitRequest,
    GetDistrict,
    UpdatePositionView,
    UpdatePermitStatus)

urlpatterns = [
    path('trader/', Trader.as_view(), name='trader'),
    path('permit/<int:permitId>/', ViewPermit.as_view(), name='permit'),
    path('trader_profile/', TraderProfile.as_view(), name='trader_profile'),
    path('get_district/', GetDistrict.as_view(), name='get_district'),
    path('update_position/<int:permit_id>/', UpdatePositionView.as_view(), name='update_position'),
    path('permit_request/', MakePermitRequest.as_view(), name='permit_request'),
    path('update_permit_status/<int:permit_id>/', UpdatePermitStatus.as_view(), name='update_permit_status'),
]
