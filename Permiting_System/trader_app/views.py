from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.views.generic import View
from .models import License
from django.apps import apps
from components.generate_qr_code import GenerateQRCodeMixin
from django.contrib import messages
import base64


class Trader(LoginRequiredMixin, View):
    template_name = 'trader_app/trader.html'

    def get(self, request):
        if request.user.userprofile.is_trader:
            license = License.objects.filter(user=request.user).first()
            if license:
                permit_model = apps.get_model('dvo_app', 'Permit')
                permits = permit_model.objects.filter(license_id=license)
            else:
                permits = []
            return render(request, self.template_name, context={'license': license, 'permits': permits})
        else:
            return HttpResponseForbidden(f"You are authenticated as {request.user}, but are not authorized to access this page.")


class TraderProfile(LoginRequiredMixin, View):
    template_name = 'trader_app/profile.html'

    def get(self, request):
        if request.user.userprofile.is_trader:
            return render(request, self.template_name, context={})
        else:
            return HttpResponseForbidden(f"You are authenticated as {request.user}, but are not authorized to access this page.")


class ViewLicense(LoginRequiredMixin, View):
    model = License
    template = 'trader_app/license.html'

    def get(self, request):
        if request.user.is_authenticated:
            queryset = self.model.objects.filter(user=request.user)
            license = queryset
            return render(request, self.template, context={'license': license})


class ViewPermit(LoginRequiredMixin, GenerateQRCodeMixin, View):
    model = apps.get_model('dvo_app', 'Permit')
    template = 'trader_app/permit.html'

    def get(self, request, permitId):
        permit = self.model.objects.get(id=permitId)

        permit_data = {
            'permitId': permitId,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name
        }
        permit_qr_code_image_data = self.generate_qr_code(permit_data)
        permit_base64_image_data = base64.b64encode(permit_qr_code_image_data).decode('utf-8')

        try:
            AnimalInfo = apps.get_model('dvo_app', 'AnimalInfo')
            animal_info = AnimalInfo.objects.get(permit=permit)
        except AnimalInfo.DoesNotExist:
            messages.error(request, 'Animal permit does not exist')
            return render(request, self.template, context={'permit': permit, 'permit_base64_image_data': permit_base64_image_data})

        animal_info_data = {'id': animal_info.id, 'animal': animal_info.animal.type}
        animal_qr_code_image_data = self.generate_qr_code(animal_info_data)
        animal_base64_image_data = base64.b64encode(animal_qr_code_image_data).decode('utf-8')

        context = {
            'permit': permit,
            'animal_info': animal_info,
            'permit_base64_image_data': permit_base64_image_data,
            'animal_base64_image_data': animal_base64_image_data
        }
        return render(request, self.template, context)
