from django.db import models
from django.contrib.auth.models import User
from staff_app.models import Trader
from staff_app.models import District
from datetime import datetime, timedelta
import enum


class Animal(models.Model):
    animal_img = models.ImageField(
        null=True,
        blank=True,
        upload_to='animal')
    type = models.CharField(max_length=30)

    def __str__(self):
        return f'Animal Type {self.type}'


class DocumentChoices(str, enum.Enum):
    VALID = "Valid"
    EXPIRED = "Expired"
    IN_TRANSIT = "In Transit"

    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)


class Permit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE)
    source = models.ForeignKey(District, related_name='permits_as_source', on_delete=models.CASCADE)
    destination = models.ForeignKey(District, related_name='permits_as_destination', on_delete=models.CASCADE)
    purpose = models.CharField(max_length=30)
    status = models.CharField(
        max_length=15,
        choices=DocumentChoices.choices(),
        default=DocumentChoices.VALID.value
    )
    date_of_expiry = models.DateField(
        default=datetime.now() + timedelta(days=1)
        )
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.date_of_expiry = datetime.now() + timedelta(days=1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Permit for \
        {self.trader.first_name} {self.trader.last_name}'


class AnimalInfo(models.Model):
    permit = models.ForeignKey(Permit, on_delete=models.CASCADE)
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    sex = models.CharField(max_length=1, default="M")
    color = models.CharField(max_length=30, default="black")
    quantity = models.IntegerField()
    date_of_expiry = models.DateField(
        default=datetime.now() + timedelta(days=1)
        )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.date_of_expiry = datetime.now() + timedelta(days=1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Information for animals of \
        {self.trader.first_name} {self.trader.last_name}'
