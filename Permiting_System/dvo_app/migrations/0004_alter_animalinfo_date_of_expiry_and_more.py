# Generated by Django 5.0.6 on 2024-06-10 17:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dvo_app', '0003_alter_animalinfo_date_of_expiry_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animalinfo',
            name='date_of_expiry',
            field=models.DateField(default=datetime.datetime(2024, 6, 11, 20, 55, 40, 131325)),
        ),
        migrations.AlterField(
            model_name='permit',
            name='date_of_expiry',
            field=models.DateField(default=datetime.datetime(2024, 6, 11, 20, 55, 40, 131325)),
        ),
    ]
