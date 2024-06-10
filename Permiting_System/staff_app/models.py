from django.db import models
import enum


class Quarantine(models.Model):
    district = models.CharField(max_length=30)
    animal = models.CharField(max_length=30)


class ApplicantChoices(str, enum.Enum):
    a = "Approved"
    b = "Rejected"
    c = "Submitted"

    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)


class Applicant(models.Model):
    profile_picture = models.ImageField(
        null=True,
        blank=True,
        upload_to='profile_pictures')
    nin = models.CharField(max_length=30, unique=True)
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
    status = models.CharField(
        max_length=1,
        choices=ApplicantChoices.choices()
        )
