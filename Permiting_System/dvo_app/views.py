from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.views.generic import View
from .models import Permit, Animal, AnimalInfo
from django.apps import apps


class DVO(LoginRequiredMixin, View):
    model = apps.get_model('staff_app', 'Quarantine')
    template_name = 'dvo_app/dvo.html'

    def get(self, request):
        user = request.user
        district = user.userprofile.district

        if not user.userprofile.is_dvo:
            return HttpResponseForbidden(f"You are authenticated as {request.user}, but are not authorized to access this page.")

        quarantine_exists = self.model.objects.filter(district=district).exists()
        if quarantine_exists:
            messages.error(request, f'Quarantine is imposed in {district}')

        try:
            permit_requests_model = apps.get_model('trader_app', 'PermitRequest')
            permit_requests = permit_requests_model.objects.filter(district=district, status='b')
        except permit_requests_model.DoesNotExist:
            permit_requests = []
            messages.error(request, 'No permit requests found')

        context = {'permit_requests': permit_requests}
        return render(request, self.template_name, context)


class DVOProfile(LoginRequiredMixin, View):
    template_name = 'dvo_app/profile.html'

    def get(self, request):
        user = request.user

        if user.userprofile.is_dvo:
            return render(request, self.template_name, context={})


class ViewPermitRequestDetails(LoginRequiredMixin, View):
    model = apps.get_model('trader_app', 'PermitRequest')
    template_name = 'dvo_app/permit_request.html'

    def get(self, request, request_id):
        permit_request = self.model.objects.get(id=request_id)
        return render(request, self.template_name, context={'permit_request': permit_request})


class GeneratePermit(LoginRequiredMixin, View):
    model = apps.get_model('staff_app', 'Quarantine')
    template_name = 'dvo_app/permit_request.html'

    def get(self, request):
        return render(request, self.template_name, context={})

    def post(self, request):
        user = request.user
        district = user.userprofile.district
        license_id = request.POST.get('license_id')
        request_id = request.POST.get('request_id')
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        purpose = request.POST.get('purpose')
        quantity = request.POST.get('quantity')
        animal_type = request.POST.get('animal_type')
        status = 'a'

        try:
            trader = apps.get_model('staff_app', 'Trader')
            trader = trader.objects.get(license_id=license_id)
        except trader.DoesNotExist:
            messages.error(request, 'License does not exist')
            return render(request, self.template_name, context={})

        try:
            animal = Animal.objects.get(type=animal_type)
        except animal.DoesNotExist:
            messages.error(request, f'{animal_type} does not exist')
            return render(request, self.template_name, context={})

        queryset = self.model.objects.filter(district=district, animal=animal).exists()
        if queryset:
            messages.error(request, f'Cannot generate Permit because a Quarantine for {animal} is imposed in {district}')
            return render(request, self.template_name, context={})

        try:
            permit_request_model = apps.get_model('trader_app', 'PermitRequest')
            permit_request = permit_request_model.objects.get(id=request_id)
            permit_request.status = 'a'
            permit_request.save()

            permit = Permit.objects.create(
                user=user,
                trader=trader,
                source=source,
                destination=destination,
                purpose=purpose,
                status=status
            )

            AnimalInfo.objects.create(
                permit=permit,
                trader=trader,
                animal=animal,
                quantity=quantity
            )
            return redirect('dvo:dvo')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, self.template_name, context={})
