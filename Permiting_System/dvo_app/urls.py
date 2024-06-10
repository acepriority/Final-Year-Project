from django.urls import path
from .views import DVO, ViewPermitRequestDetails, GeneratePermit, DVOProfile


urlpatterns = [
    path('dvo/', DVO.as_view(), name='dvo'),
    path('permit_request_details/<int:request_id>/', ViewPermitRequestDetails.as_view(), name='permit_request_details'),
    path('generate_permit/', GeneratePermit.as_view(), name='generate_permit'),
    path('dvo_profile/', DVOProfile.as_view(), name='dvo_profile')
]
