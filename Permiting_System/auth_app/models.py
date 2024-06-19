from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_picture = models.ImageField(
        null=True,
        upload_to='profile_pictures')
    is_staff = models.BooleanField(default=False)
    is_dvo = models.BooleanField(default=False)
    is_trader = models.BooleanField(default=False)
    nin = models.CharField(max_length=30, unique=True)
    sex = models.CharField(max_length=1)
    date_of_birth = models.DateField()
    telephone = models.IntegerField(unique=True)
    village = models.CharField(max_length=30)
    parish = models.CharField(max_length=30)
    s_county = models.CharField(max_length=30)
    county = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
