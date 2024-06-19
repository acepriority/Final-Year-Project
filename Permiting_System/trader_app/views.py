from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, JsonResponse
from django.views.generic import View
from django.apps import apps
from django.contrib.auth.models import User
from components.generate_qr_code import GenerateQRCodeMixin
from django.contrib import messages
import base64
from .models import PermitRequest
from auth_app.utils import URLBuilder
import logging

logger = logging.getLogger(__name__)


class Trader(LoginRequiredMixin, View):
    template_name = 'trader_app/trader.html'
    model = apps.get_model('staff_app', 'TraderLicense')

    def get(self, request):
        user_profile = request.user.userprofile
        if user_profile.is_trader:
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            license_id = self.model.get_license_id_for_user(user)

            trader_model = apps.get_model('staff_app', 'Trader')
            trader, permits = trader_model.get_trader_with_permits(license_id)
            if trader:
                return render(request, self.template_name, context={'trader': trader, 'permits': permits})
            else:
                logger.error(f'Trader with ID {license_id} not found.')
                return HttpResponseForbidden(f"{trader} profile not found.")
        else:
            logger.warning(f'Unauthorized access attempt by user {request.user.username}.')
            return HttpResponseForbidden(f"You are authenticated as {request.user}, but are not authorized to access this page.")


class TraderProfile(LoginRequiredMixin, View):
    template_name = 'trader_app/profile.html'

    def get(self, request):
        if request.user.userprofile.is_trader:
            return render(request, self.template_name, context={})
        else:
            return HttpResponseForbidden(f"You are authenticated as {request.user}, but are not authorized to access this page.")


class ViewPermit(LoginRequiredMixin, GenerateQRCodeMixin, View):
    model = apps.get_model('dvo_app', 'Permit')
    template = 'trader_app/permit.html'

    def get(self, request, permitId):
        permit = self.model.objects.get(id=permitId)

        url_builder = URLBuilder(request)
        url = url_builder.build_url('trader:permit', permitId=permitId)

        permit_data = url
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


class MakePermitRequest(LoginRequiredMixin, View):
    model = PermitRequest
    template_name = 'trader_app/make_permit_request.html'

    def get(self, request):
        model = apps.get_model('staff_app', 'TraderLicense')
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        license_id = model.get_license_id_for_user(user)
        return render(request, self.template_name, context={'license_id': license_id})

    def post(self, request):
        user = request.user
        license_id = request.POST.get('license_id')
        animal_type = request.POST.get('animal_type')
        quantity = request.POST.get('quantity')
        district = request.POST.get('district')
        lc1_letter = request.FILES.get('lc1_letter')
        status = 'b'

        try:
            Animal = apps.get_model('dvo_app', 'Animal')
            animal = Animal.objects.get(type=animal_type)
            self.model.objects.create(
                user=user,
                license_id=license_id,
                animal_type=animal,
                quantity=quantity,
                district=district,
                lc1_letter=lc1_letter,
                status=status
            )
            return HttpResponseForbidden(f"Permit request by {user} created successfully.")
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
