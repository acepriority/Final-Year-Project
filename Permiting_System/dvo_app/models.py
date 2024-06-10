from django.db import models
from django.contrib.auth.models import User
from trader_app.models import License
from datetime import datetime, timedelta
import enum


class Animal(models.Model):
    type = models.CharField(max_length=30)


class DocumentChoices(str, enum.Enum):
    a = "Valid"
    b = "Expired"

    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)


class Permit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    license = models.ForeignKey(License, on_delete=models.CASCADE)
    source = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)
    purpose = models.CharField(max_length=30)
    status = models.CharField(
        max_length=1,
        choices=DocumentChoices.choices()
        )
    date_of_expiry = models.DateField(
        default=datetime.now() + timedelta(days=1)
        )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.date_of_expiry = datetime.now() + timedelta(days=1)
        super().save(*args, **kwargs)


class AnimalInfo(models.Model):
    permit = models.ForeignKey(Permit, on_delete=models.CASCADE)
    license = models.ForeignKey(License, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date_of_expiry = models.DateField(
        default=datetime.now() + timedelta(days=1)
        )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.date_of_expiry = datetime.now() + timedelta(days=1)
        super().save(*args, **kwargs)
