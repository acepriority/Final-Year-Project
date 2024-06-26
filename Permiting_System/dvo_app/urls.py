from django.urls import path
from .views import (
    DVO,
    ViewPermitRequestDetails,
    GeneratePermit,
    DVOProfile,
    ViewPermit)


urlpatterns = [
    path('dvo/', DVO.as_view(), name='dvo'),
    path('dvo_profile/', DVOProfile.as_view(), name='dvo_profile'),
    path('permit_request_details/<int:request_id>/', ViewPermitRequestDetails.as_view(), name='permit_request_details'),
    path('generate_permit/', GeneratePermit.as_view(), name='generate_permit'),
    path('permit/<int:permitId>/', ViewPermit.as_view(), name='permit'),
]
