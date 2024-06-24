# Generated by Django 5.0.6 on 2024-06-21 10:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dvo_app', '0003_alter_animalinfo_date_of_expiry_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='animal_img',
            field=models.ImageField(blank=True, null=True, upload_to='animal'),
        ),
        migrations.AlterField(
            model_name='animalinfo',
            name='date_of_expiry',
            field=models.DateField(default=datetime.datetime(2024, 6, 22, 13, 9, 9, 642250)),
        ),
        migrations.AlterField(
            model_name='permit',
            name='date_of_expiry',
            field=models.DateField(default=datetime.datetime(2024, 6, 22, 13, 9, 9, 642250)),
        ),
    ]
