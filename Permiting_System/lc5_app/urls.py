from django.urls import path
from lc5_app.views import LC5, MakePermitRequest, LC5Profile

urlpatterns = [
    path('lc5/', LC5.as_view(), name='lc5'),
    path('permit_request/', MakePermitRequest.as_view(), name='permit_request'),
    path('lc5_profile/', LC5Profile.as_view(), name='lc5_profile')
]
