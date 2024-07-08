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
from collections import Counter
from collections import defaultdict
import calendar


class Staff(StaffRequiredMixin, View):
    template_name = 'staff_app/staff.html'


class StaffProfile(StaffRequiredMixin, View):
    template_name = 'staff_app/profile.html'


class ViewUsersTable(LoginRequiredMixin, ViewTablesMixin, View):
    def __init__(self):
        model = apps.get_model('auth_app', 'UserProfile')
        template = 'staff_app/userstable.html'
        super().__init__(model=model, template=template)


class ViewQuarantineTable(LoginRequiredMixin, ViewTablesMixin, View):
    def __init__(self):
        super().__init__(model=Quarantine, template='staff_app/quarantinetables.html')


class ViewPermitstable(LoginRequiredMixin, ViewTablesMixin, View):
    def __init__(self):
        model = apps.get_model('dvo_app', 'Permit')
        super().__init__(model=model, template='staff_app/permitstable.html')

    def get_context_data(self) -> dict:
        queryset = self.model.objects.order_by('-id')

        permits_per_user = {}
        sources = []
        destinations = []
        for permit in queryset:
            name = f'{permit.trader.first_name}'
            if name not in permits_per_user:
                permits_per_user[name] = 0
            permits_per_user[name] += 1
            sources.append(permit.source)
            destinations.append(permit.destination)

        labels = list(permits_per_user.keys())
        data = list(permits_per_user.values())

        total_permits = sum(data)
        most_common_source = Counter(sources).most_common(1)[0][0]
        most_common_destination = Counter(destinations).most_common(1)[0][0]

        context = super().get_context_data()
        context.update({
            'labels': labels,
            'data': data,
            'total_permits': total_permits,
            'most_common_source': most_common_source,
            'most_common_destination': most_common_destination,
        })
        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context=context)


class ViewLicensesTable(ViewTablesMixin, View):
    def __init__(self):
        model = apps.get_model('staff_app', 'TraderLicense')
        super().__init__(model=model, template='staff_app/licensestable.html')


class ViewPermitRequeststable(LoginRequiredMixin, ViewTablesMixin, View):
    def __init__(self):
        model = apps.get_model('trader_app', 'PermitRequest')
        super().__init__(model=model, template='staff_app/permitrequeststable.html')


class ViewApplicantsTable(LoginRequiredMixin, ViewTablesMixin, View):
    def __init__(self):
        model = apps.get_model('staff_app', 'Trader')
        super().__init__(model=model, template='staff_app/applicantstable.html')

    def get_context_data(self) -> dict:
        queryset = self.model.objects.order_by('-id')

        traders_per_month = defaultdict(int)
        districts = Counter()

        for trader in queryset:
            month = calendar.month_name[trader.date_submitted.month]
            traders_per_month[month] += 1
            districts[trader.district] += 1

        labels = list(traders_per_month.keys())
        data = list(traders_per_month.values())
        total_applicants = len(queryset)
        common_district = districts.most_common(1)[0][0] if districts else None

        context = super().get_context_data()
        context.update({
            'labels': labels,
            'data': data,
            'total_applicants': total_applicants,
            'common_district': common_district,
        })
        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context=context)


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
