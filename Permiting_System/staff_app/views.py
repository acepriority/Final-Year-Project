from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .utils import ViewTablesMixin, StaffRequiredMixin
from django.apps import apps
from .models import ApplicantChoices, Trader
from django.contrib.auth.models import User
from django.utils import timezone
from components.email import SendEmailMixin
import random
import string
from .models import Quarantine


class Staff(StaffRequiredMixin, View):
    template_name = 'staff_app/staff.html'


class StaffProfile(StaffRequiredMixin, View):
    template_name = 'staff_app/profile.html'


class ViewUsersTable(LoginRequiredMixin, ViewTablesMixin, View):
    def __init__(self):
        model = apps.get_model('auth_app', 'UserProfile')
        super().__init__(model=model, template='staff_app/userstable.html')


class ViewQuarantineTable(LoginRequiredMixin, ViewTablesMixin, View):
    def __init__(self):
        super().__init__(model=Quarantine, template='staff_app/quarantinetables.html')


class ViewPermitstable(LoginRequiredMixin, ViewTablesMixin, View):
    def __init__(self):
        model = apps.get_model('dvo_app', 'Permit')
        super().__init__(model=model, template='staff_app/permitstable.html')


class ViewLicensesTable(ViewTablesMixin, View):
    def __init__(self):
        model = apps.get_model('staff_app', 'TraderLicense')
        super().__init__(model=model, template='staff_app/licensestable.html')


class ViewPermitRequeststable(LoginRequiredMixin, ViewTablesMixin, View):
    def __init__(self):
        model = apps.get_model('lc5_app', 'PermitRequest')
        super().__init__(model=model, template='staff_app/permitrequeststable.html')


class ViewApplicantsTable(LoginRequiredMixin, ViewTablesMixin, View):
    def __init__(self):
        model = apps.get_model('staff_app', 'Trader')
        super().__init__(model=model, template='staff_app/applicantstable.html')


class ApplicantDetails(LoginRequiredMixin, View):
    model = Trader
    template_name = 'staff_app/applicant_detail.html'

    def get(self, request, applicant_id):
        applicant = self.model.objects.get(id=applicant_id)
        return render(request, self.template_name, context={'applicant': applicant})


class RejectApplicant(LoginRequiredMixin, SendEmailMixin, View):
    model = Trader
    template = 'staff_app/staff.html'

    def post(self, request, applicant_id):
        applicant = self.model.objects.get(id=applicant_id)
        reason = request.POST.get('reason')
        self.send_rejection_email(request, reason, applicant_id, applicant.email)

        applicant.status = ApplicantChoices.b.name
        applicant.date_rejected = timezone.now()
        applicant.save()
        return render(request, self.template, context={})

    def get(self, request, applicant_id):
        return render(request, self.template, context={})


class ApproveApplicant(LoginRequiredMixin, SendEmailMixin, View):
    model = Trader
    template_name = 'staff_app/staff.html'

    def get(self, request, applicant_id):
        applicant = self.model.objects.get(id=applicant_id)
        username = f"@{applicant.first_name.lower()}{applicant.last_name.lower().replace(' ', '')}"

        counter = 1
        while User.objects.filter(username=username).exists():
            username = f'@{applicant.first_name.lower()}{applicant.last_name.lower()}{counter}'
            counter += 1

        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

        user = User.objects.create_user(
            first_name=applicant.first_name,
            last_name=applicant.last_name,
            username=username,
            email=applicant.email,
            password=password)

        user_profile_model = apps.get_model('auth_app', 'UserProfile')
        user_profile = user_profile_model(
            user=user,
            is_staff=False,
            is_dvo=False,
            is_trader=True,
            profile_picture=applicant.profile_picture,
            nin=applicant.nin,
            sex=applicant.sex,
            date_of_birth=applicant.date_of_birth,
            telephone=applicant.telephone,
            village=applicant.village,
            parish=applicant.parish,
            s_county=applicant.s_county,
            county=applicant.county,
            district=applicant.district,
        )

        user_profile.save()

        trader_model = apps.get_model('staff_app', 'TraderLicense')
        trader_model.objects.create(
            user=user,
            trader=applicant
        )

        self.send_approval_email(request, username, password, applicant.email)

        applicant.status = ApplicantChoices.a.name
        applicant.date_approved = timezone.now()
        applicant.save()
        return render(request, self.template_name, context={})

    def post(self, request):
        return render(request, self.template_name, context={})


class QuarantineDetails(LoginRequiredMixin, View):
    model = Quarantine
    template_name = 'staff_app/quarantine_details.html'

    def get(self, request, id):
        quarantine = self.model.objects.get(id=id)
        return render(request, self.template_name, context={'quarantine': quarantine})


class ImposeQuarantine(LoginRequiredMixin, View):
    model = Quarantine
    template_name = 'staff_app/quarantine.html'

    def get(self, request):
        return render(request, self.template_name, context={})

    def post(self, request):
        district = request.POST.get('district')
        animal = request.POST.get('animal')

        self.model.objects.create(
            district=district,
            animal=animal
        )

        return redirect('staff:quarantinetable')


class RemoveQuarantine(LoginRequiredMixin, View):
    model = Quarantine

    def get(self, request, id):
        quarantine_object = get_object_or_404(self.model, id=id)
        quarantine_object.delete()
        return redirect('staff:quarantinetable')
