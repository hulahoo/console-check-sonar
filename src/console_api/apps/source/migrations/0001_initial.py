# Generated by Django 4.0.4 on 2022-12-16 15:27

import console_api.apps.common.enums
import console_api.apps.models.abstract
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', console_api.apps.models.abstract.CreationDateTimeField(auto_now_add=True, verbose_name='создано')),
                ('updated_at', console_api.apps.models.abstract.ModificationDateTimeField(auto_now=True, verbose_name='изменено')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('is_instead_full', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('provider_name', models.CharField(max_length=255)),
                ('path', models.TextField()),
                ('certificate', models.FileField(blank=True, null=True, upload_to='', verbose_name='Путь к сертификату')),
                ('authenticity', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='Достоверность')),
                ('format', models.CharField(choices=[('STIX', 'STIX'), ('MISP', 'MISP'), ('FREE_TEXT', 'FREE_TEXT'), ('JSON', 'JSON'), ('CSV', 'CSV')], default=console_api.apps.common.enums.FormatTypeEnum['CSV'], max_length=17, verbose_name='Формат')),
                ('auth_type', models.CharField(choices=[('NO_AUTH', 'NAU'), ('API', 'API'), ('BASIC', 'BSC')], default=console_api.apps.common.enums.AuthEnum['NO_AUTH'], max_length=17, verbose_name='Тип авторизации')),
                ('auth_login', models.CharField(blank=True, max_length=32, null=True, verbose_name='Логин для авторизации')),
                ('auth_password', models.CharField(blank=True, max_length=64, null=True, verbose_name='Пароль для авторизации')),
                ('max_rows', models.IntegerField(default=None, null=True)),
                ('raw_indicators', models.TextField(default=None, null=True)),
                ('update_time_period', models.PositiveBigIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Источник',
                'verbose_name_plural': 'Источники',
                'db_table': 'sources',
            },
        ),
    ]
