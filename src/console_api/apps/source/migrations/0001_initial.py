# Generated by Django 4.0.4 on 2022-12-06 11:55

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import apps.common.enums
import apps.models.abstract


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('indicator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', apps.models.abstract.CreationDateTimeField(auto_now_add=True, verbose_name='создано')),
                ('modified', apps.models.abstract.ModificationDateTimeField(auto_now=True, verbose_name='изменено')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', apps.models.abstract.CreationDateTimeField(auto_now_add=True, verbose_name='создано')),
                ('modified', apps.models.abstract.ModificationDateTimeField(auto_now=True, verbose_name='изменено')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('is_instead_full', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('provider_name', models.CharField(max_length=255)),
                ('path', models.TextField()),
                ('certificate', models.FileField(blank=True, null=True, upload_to='', verbose_name='Путь к сертификату')),
                ('authenticity', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='Достоверность')),
                ('format', models.CharField(choices=[('STIX', 'STIX'), ('MISP', 'MISP'), ('FREE_TEXT', 'FREE_TEXT'), ('JSON', 'JSON'), ('CSV', 'CSV')], default=apps.common.enums.FormatTypeEnum['CSV'], max_length=17, verbose_name='Формат')),
                ('auth_type', models.CharField(choices=[('NO_AUTH', 'NAU'), ('API', 'API'), ('BASIC', 'BSC')], default=apps.common.enums.AuthEnum['NO_AUTH'], max_length=17, verbose_name='Тип авторизации')),
                ('auth_login', models.CharField(blank=True, max_length=32, null=True, verbose_name='Логин для авторизации')),
                ('auth_password', models.CharField(blank=True, max_length=64, null=True, verbose_name='Пароль для авторизации')),
                ('max_rows', models.IntegerField(default=None, null=True)),
                ('raw_indicators', models.TextField(default=None, null=True)),
                ('update_time_period', models.PositiveBigIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Источник',
                'verbose_name_plural': 'Источники',
            },
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', apps.models.abstract.CreationDateTimeField(auto_now_add=True, verbose_name='создано')),
                ('modified', apps.models.abstract.ModificationDateTimeField(auto_now=True, verbose_name='изменено')),
                ('comment', models.TextField()),
                ('activity_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='source.activitytype')),
                ('indicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='indicator.indicator')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]