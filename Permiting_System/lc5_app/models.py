from django.db import models
from django.contrib.auth.models import User
from trader_app.models import License
from dvo_app.models import Animal
import enum


class DocumentChoices(str, enum.Enum):
    a = "Processed"
    b = "Pending"

    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)


class PermitRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    license_id = models.ForeignKey(License, on_delete=models.CASCADE)
    animal_type = models.ForeignKey(Animal, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    lc1_letter = models.ImageField(
        null=True,
        upload_to='lc1_letters')
    status = models.CharField(
        max_length=1,
        choices=DocumentChoices.choices(),
        )

    def __str__(self):
        return f'PermitRequest by {self.user.username}'
