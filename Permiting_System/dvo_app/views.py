from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.views.generic import View
from django.apps import apps
from components.generate_qr_code import GenerateQRCodeMixin
import base64
from django.core.serializers import serialize
import json
from components.email import SendEmailMixin


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


class GeneratePermit(LoginRequiredMixin, SendEmailMixin, View):
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
        status = 'a'

        animal_types = request.POST.getlist('animal_type')
        sexes = request.POST.getlist('sex')
        colors = request.POST.getlist('color')
        quantities = request.POST.getlist('quantity')

        try:
            trader_model = apps.get_model('staff_app', 'Trader')
            trader = trader_model.objects.get(license_id=license_id)
        except trader_model.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'License does not exist'}, status=400)

        animal_model = apps.get_model('dvo_app', 'Animal')
        animal_info_model = apps.get_model('dvo_app', 'AnimalInfo')
        quarantine_model = apps.get_model('staff_app', 'Quarantine')

        try:
            for animal_type, sex, color, quantity in zip(animal_types, sexes, colors, quantities):
                animal, created = animal_model.objects.get_or_create(type=animal_type)

                if quarantine_model.objects.filter(district=district, animal=animal).exists():
                    return JsonResponse({'success': False, 'error': f'Cannot generate Permit because a Quarantine for {animal.type} is imposed in {district}'}, status=400)

            permit_request_model = apps.get_model('trader_app', 'PermitRequest')
            permit_request = permit_request_model.objects.get(id=request_id)
            permit_request.status = 'a'
            permit_request.save()

            permit_model = apps.get_model('dvo_app', 'Permit')
            permit = permit_model.objects.create(
                user=user,
                trader=trader,
                source=source,
                destination=destination,
                purpose=purpose,
                status=status
            )

            self.send_permit_email(request, trader.email, permit.id)

            for animal_type, sex, color, quantity in zip(animal_types, sexes, colors, quantities):
                animal = animal_model.objects.get(type=animal_type)
                animal_info_model.objects.create(
                    permit=permit,
                    trader=trader,
                    animal=animal,
                    sex=sex,
                    color=color,
                    quantity=quantity
                )

            permit_data = json.loads(serialize('json', [permit]))[0]['fields']
            permit_data['id'] = permit.id

            return JsonResponse({'success': True, 'permit': permit_data})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


class ViewPermit(LoginRequiredMixin, GenerateQRCodeMixin, View):
    model = apps.get_model('dvo_app', 'Permit')
    template = 'dvo_app/permit.html'

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
            'total_animals': total_animals
        }
        return render(request, self.template, context)
