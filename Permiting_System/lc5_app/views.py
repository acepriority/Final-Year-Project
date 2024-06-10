from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import View
from .models import PermitRequest
from trader_app.models import License
from dvo_app.models import Animal
from lc5_app.utils import LC5RequiredMixin


class LC5(LC5RequiredMixin, View):
    template_name = 'lc5_app/lc5.html'


class LC5Profile(LC5RequiredMixin, View):
    template_name = 'lc5_app/profile.html'


class MakePermitRequest(LoginRequiredMixin, View):
    model = PermitRequest

    def post(self, request):
        user = request.user
        license_id = request.POST.get('license_id')
        animal_type = request.POST.get('animal_type')
        quantity = request.POST.get('quantity')
        lc1_letter = request.FILES.get('lc1_letter')
        status = 'b'

        try:
            license_id = License.objects.get(pk=license_id)
            animal = Animal.objects.get(type=animal_type)
            self.model.objects.create(
                user=user,
                license_id=license_id,
                animal_type=animal,
                quantity=quantity,
                lc1_letter=lc1_letter,
                status=status
            )
            return JsonResponse(
                {'message': 'Permit request created successfully.'}
                )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
