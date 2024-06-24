from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.apps import apps
from .utils import ViewIndexPages
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from components.generate_qr_code import GenerateQRCodeMixin
import base64
from auth_app.utils import URLBuilder
from django.contrib import messages


class Index(ViewIndexPages, View):
    def __init__(self):
        super().__init__(template_name='index_app/indexpage.html')


class Apply(ViewIndexPages, View):
    def __init__(self):
        super().__init__(template_name='index_app/applypage.html')


class About(ViewIndexPages, View):
    def __init__(self):
        super().__init__(template_name='index_app/aboutpage.html')


class Act(ViewIndexPages, View):
    def __init__(self):
        super().__init__(template_name='index_app/actpage.html')


class Login(ViewIndexPages, View):
    def __init__(self):
        super().__init__(template_name='index_app/loginpage.html')


class CreateApplicant(View):
    model = apps.get_model('staff_app', 'Trader')
    template_name = 'index_app/applypage.html'

    def post(self, request):
        profile_picture = request.FILES.get('profile_picture')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        nin = request.POST.get('nin')
        license_id = request.POST.get('license_id')
        date_of_birth = request.POST.get('date_of_birth')
        sex = request.POST.get('sex')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        village = request.POST.get('village')
        parish = request.POST.get('parish')
        s_county = request.POST.get('s_county')
        county = request.POST.get('county')
        district = request.POST.get('district')
        status = 'c'

        self.model.objects.create(
            first_name=first_name,
            last_name=last_name,
            nin=nin,
            license_id=license_id,
            date_of_birth=date_of_birth,
            sex=sex,
            email=email,
            telephone=telephone,
            village=village,
            parish=parish,
            s_county=s_county,
            county=county,
            district=district,
            status=status,
            profile_picture=profile_picture
        )
        return redirect('apply')

    def get(self, request):
        return render(request, self.template_name, context={})


class UpdateApplicantDetails(View):
    model = apps.get_model('staff_app', 'Trader')
    template_name = 'index_app/update_details.html'

    def get(self, request, applicant_id):
        applicant = get_object_or_404(self.model, id=applicant_id)
        return render(request, self.template_name, {'applicant': applicant})

    def post(self, request, applicant_id):
        applicant = get_object_or_404(self.model, id=applicant_id)

        applicant.profile_picture = request.FILES.get('profile_picture')
        applicant.first_name = request.POST.get('first_name')
        applicant.last_name = request.POST.get('last_name')
        applicant.nin = request.POST.get('nin')
        applicant.license_id = request.POST.get('license_id')
        applicant.date_of_birth = request.POST.get('date_of_birth')
        applicant.sex = request.POST.get('sex')
        applicant.email = request.POST.get('email')
        applicant.telephone = request.POST.get('telephone')
        applicant.village = request.POST.get('village')
        applicant.parish = request.POST.get('parish')
        applicant.s_county = request.POST.get('s_county')
        applicant.county = request.POST.get('county')
        applicant.district = request.POST.get('district')
        applicant.status = 'c'

        applicant.save()
        return redirect('index')


class DisplayPermit(GenerateQRCodeMixin, View):
    template_name = 'index_app/permit.html'

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
