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
import json
from django.db.models import F, Func, FloatField, ExpressionWrapper
from django.db.models.functions import Sqrt, Power, Sin, Cos, Radians, ATan2
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from dvo_app.models import DocumentChoices
from django.utils import timezone
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

        url = f'http://178.128.28.119:8080/display/{permitId}'

        permit_data = url
        permit_qr_code_image_data = self.generate_qr_code(permit_data)
        permit_base64_image_data = base64.b64encode(permit_qr_code_image_data).decode('utf-8')

        try:
            AnimalInfo = apps.get_model('dvo_app', 'AnimalInfo')
            animal_info_list = AnimalInfo.objects.filter(permit=permit)
        except AnimalInfo.DoesNotExist:
            messages.error(request, 'Animal permit does not exist')
            return render(request, self.template, context={'permit': permit, 'permit_base64_image_data': permit_base64_image_data})

        animal_info_data = url
        animal_qr_code_image_data = [self.generate_qr_code(info) for info in animal_info_data]
        animal_base64_image_data = [base64.b64encode(qr_code).decode('utf-8') for qr_code in animal_qr_code_image_data]

        zipped_animal_info = zip(animal_info_list, animal_base64_image_data)

        total_animals = sum(animal_info.quantity for animal_info in animal_info_list)

        context = {
            'permit': permit,
            'zipped_animal_info': zipped_animal_info,
            'permit_base64_image_data': permit_base64_image_data,
            'total_animals': total_animals,
            'permit_status': permit.status,
            'source_coordinates': {
                'latitude': permit.source.latitude,
                'longitude': permit.source.longitude
            },
            'destination_coordinates': {
                'latitude': permit.destination.latitude,
                'longitude': permit.destination.longitude
            }
        }
        return render(request, self.template, context)


class HaversineDistance(Func):
    function = 'HaversineDistance'
    output_field = FloatField()

    def __init__(self, lat1, lon1, lat2, lon2, **extra):
        super().__init__(lat1, lon1, lat2, lon2, **extra)
        self.template = """
        6371 * 2 * ASIN(SQRT(
            POWER(SIN(RADIANS(%(lat1)s - %(lat2)s) / 2), 2) +
            COS(RADIANS(%(lat1)s)) * COS(RADIANS(%(lat2)s)) *
            POWER(SIN(RADIANS(%(lon1)s - %(lon2)s) / 2), 2)
        ))
        """


@method_decorator(csrf_exempt, name='dispatch')
class GetDistrict(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if latitude is not None and longitude is not None:
            model = apps.get_model('staff_app', 'District')
            nearest_district = model.objects.annotate(
                distance=ExpressionWrapper(
                    6371 * 2 * ATan2(
                        Sqrt(
                            Power(Sin(Radians(F('latitude') - latitude) / 2), 2) +
                            Cos(Radians(F('latitude'))) * Cos(Radians(latitude)) *
                            Power(Sin(Radians(F('longitude') - longitude) / 2), 2)
                        ),
                        Sqrt(
                            1 - (
                                Power(Sin(Radians(F('latitude') - latitude) / 2), 2) +
                                Cos(Radians(F('latitude'))) * Cos(Radians(latitude)) *
                                Power(Sin(Radians(F('longitude') - longitude) / 2), 2)
                            )
                        )
                    ),
                    output_field=FloatField()
                )
            ).order_by('distance').first()

            if nearest_district:
                return JsonResponse({'success': True, 'district_name': nearest_district.name})
            else:
                return JsonResponse({'success': False, 'message': 'District not found'})

        return JsonResponse({'success': False, 'message': 'Invalid request'})


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
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@method_decorator(csrf_exempt, name='dispatch')
class UpdatePositionView(View, LoginRequiredMixin):
    model = apps.get_model('dvo_app', 'Permit')

    def post(self, request, permit_id):
        permit = self.model.objects.get(id=permit_id)
        trader = permit.trader

        if permit.status != DocumentChoices.IN_TRANSIT.value:
            return JsonResponse({'status': 'error', 'message': 'Permit is not in transit'}, status=400)

        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        trader.current_latitude = latitude
        trader.current_longitude = longitude
        trader.save()

        if (latitude == permit.destination.latitude and longitude == permit.destination.longitude):
            permit.status = DocumentChoices.EXPIRED.value
            permit.end_time = timezone.now()
            permit.save()

        return JsonResponse({'status': 'success', 'latitude': latitude, 'longitude': longitude})
