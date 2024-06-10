# Generated by Django 5.0.6 on 2024-06-10 16:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dvo_app', '0001_initial'),
        ('trader_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PermitRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('lc1_letter', models.ImageField(blank=True, null=True, upload_to='lc1_letters/')),
                ('status', models.CharField(choices=[('a', 'Processed'), ('b', 'Pending')], max_length=1)),
                ('animal_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dvo_app.animal')),
                ('license_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trader_app.license')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]