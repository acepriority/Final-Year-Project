from django.db import models
from django.contrib.auth.models import User
import enum
from django.apps import apps


class District(models.Model):
    name = models.CharField(max_length=30)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Quarantine(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    animal = models.CharField(max_length=30)

    def __str__(self):
        return f'Quarantine for {self.animal} in {self.district}'


class ApplicantChoices(str, enum.Enum):
    a = "Approved"
    b = "Rejected"
    c = "Submitted"

    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)


class Trader(models.Model):
    profile_picture = models.ImageField(
        null=True,
        blank=True,
        upload_to='profile_pictures')
    nin = models.CharField(max_length=30, unique=True)
    license_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    sex = models.CharField(max_length=1)
    date_of_birth = models.DateField()
    telephone = models.IntegerField(unique=True)
    village = models.CharField(max_length=30)
    parish = models.CharField(max_length=30)
    s_county = models.CharField(max_length=30)
    county = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    date_submitted = models.DateField(auto_now_add=True)
    date_approved = models.DateField(null=True)
    date_rejected = models.DateField(null=True)
    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(
        max_length=1,
        choices=ApplicantChoices.choices()
        )

    def __str__(self):
        return f'Registration for {self.first_name} {self.last_name}'

    @classmethod
    def get_trader_with_permits(cls, license_id):
        try:
            trader = cls.objects.get(license_id=license_id)
            Permit = apps.get_model('dvo_app', 'Permit')
            permits = Permit.objects.filter(trader=trader).order_by('-id')
            return trader, permits
        except cls.DoesNotExist:
            return None, None


class TraderLicense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE)

    def __str__(self):
        return f'License for {self.user.username}'

    def get_license_id_for_user(user):
        try:
            trader_license = TraderLicense.objects.get(user=user)
            return trader_license.trader.license_id
        except TraderLicense.DoesNotExist:
            return None
