# Generated by Django 5.0.6 on 2024-06-18 06:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dvo_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animalinfo',
            name='date_of_expiry',
            field=models.DateField(default=datetime.datetime(2024, 6, 19, 9, 59, 23, 17533)),
        ),
        migrations.AlterField(
            model_name='permit',
            name='date_of_expiry',
            field=models.DateField(default=datetime.datetime(2024, 6, 19, 9, 59, 23, 17533)),
        ),
    ]
