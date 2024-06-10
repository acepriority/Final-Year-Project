from django.urls import path
from staff_app.views import (
    Staff,
    StaffProfile,
    ViewUsersTable,
    ViewPermitstable,
    ViewLicensesTable,
    ViewPermitRequeststable,
    ViewApplicantsTable,
    ApplicantDetails,
    RejectApplicant,
    ApproveApplicant,
    ViewQuarantineTable,
    QuarantineDetails,
    ImposeQuarantine,
    RemoveQuarantine
    )

urlpatterns = [
    path('staff/', Staff.as_view(), name='staff'),
    path('staff_profile/', StaffProfile.as_view(), name='staff_profile'),
    path('userstable/', ViewUsersTable.as_view(), name='userstable'),
    path('permitstable/', ViewPermitstable.as_view(), name='permitstable'),
    path('licensestable/', ViewLicensesTable.as_view(), name='licensestable'),
    path('permitrequeststable/', ViewPermitRequeststable.as_view(), name='permitrequeststable'),
    path('applicantstable/', ViewApplicantsTable.as_view(), name='applicantstable'),
    path('applicant/<int:applicant_id>/', ApplicantDetails.as_view(), name='applicant_details'),
    path('reject/<int:applicant_id>/', RejectApplicant.as_view(), name='reject_applicant'),
    path('approve/<int:applicant_id>/', ApproveApplicant.as_view(), name='approve_applicant'),
    path('quarantinetable/', ViewQuarantineTable.as_view(), name='quarantinetable'),
    path('quarantine_details/<int:id>/', QuarantineDetails.as_view(), name='quarantine_details'),
    path('impose_quarantine/', ImposeQuarantine.as_view(), name='impose_quarantine'),
    path('remove_quarantine/<int:id>/', RemoveQuarantine.as_view(), name='remove_quarantine'),
]
