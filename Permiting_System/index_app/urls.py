from django.urls import path
from .views import (
    Index,
    Apply,
    Login,
    CreateApplicant,
    UpdateApplicantDetails,
    VerifyPermit,
    DisplayPermit
    )

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('apply/', Apply.as_view(), name='apply'),
    path('login/', Login.as_view(), name='login'),
    path('create_applicant/', CreateApplicant.as_view(), name='create_applicant'),
    path('update_details/<int:applicant_id>/', UpdateApplicantDetails.as_view(), name='update_applicant_details'),
    path('verify/', VerifyPermit.as_view(), name='verify'),
    path('display/<int:id>/', DisplayPermit.as_view(), name='display_permit'),
]
