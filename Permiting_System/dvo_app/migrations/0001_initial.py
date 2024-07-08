# Generated by Django 5.0.6 on 2024-07-07 18:52

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('staff_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('animal_img', models.ImageField(blank=True, null=True, upload_to='animal')),
                ('type', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Permit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purpose', models.CharField(max_length=30)),
                ('status', models.CharField(choices=[('a', 'Valid'), ('b', 'Expired')], max_length=1)),
                ('date_of_expiry', models.DateField(default=datetime.datetime(2024, 7, 8, 21, 52, 28, 816857))),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permits_as_destination', to='staff_app.district')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permits_as_source', to='staff_app.district')),
                ('trader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff_app.trader')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AnimalInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex', models.CharField(default='M', max_length=1)),
                ('color', models.CharField(default='black', max_length=30)),
                ('quantity', models.IntegerField()),
                ('date_of_expiry', models.DateField(default=datetime.datetime(2024, 7, 8, 21, 52, 28, 816857))),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dvo_app.animal')),
                ('trader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff_app.trader')),
                ('permit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dvo_app.permit')),
            ],
        ),
    ]
