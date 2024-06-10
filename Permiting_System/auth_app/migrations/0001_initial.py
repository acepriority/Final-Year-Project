# Generated by Django 5.0.6 on 2024-06-10 16:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_dvo', models.BooleanField(default=False)),
                ('is_lc5', models.BooleanField(default=False)),
                ('is_trader', models.BooleanField(default=False)),
                ('nin', models.CharField(max_length=30, unique=True)),
                ('sex', models.CharField(max_length=1)),
                ('date_of_birth', models.DateField()),
                ('telephone', models.IntegerField(unique=True)),
                ('village', models.CharField(max_length=30)),
                ('parish', models.CharField(max_length=30)),
                ('s_county', models.CharField(max_length=30)),
                ('county', models.CharField(max_length=30)),
                ('district', models.CharField(max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]