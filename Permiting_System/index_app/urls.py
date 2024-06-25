from django.urls import path
from .views import (
    Index,
    Apply,
    About,
    Act,
    Login,
    CreateApplicant,
    UpdateApplicantDetails,
    DisplayPermit
    )

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('apply/', Apply.as_view(), name='apply'),
    path('about/', About.as_view(), name='about'),
    path('act/', Act.as_view(), name='act'),
    path('login/', Login.as_view(), name='login'),
    path('create_applicant/', CreateApplicant.as_view(), name='create_applicant'),
    path('update_details/<int:applicant_id>/', UpdateApplicantDetails.as_view(), name='update_applicant_details'),
    path('display/<int:permitId>/', DisplayPermit.as_view(), name='display_permit'),
]
