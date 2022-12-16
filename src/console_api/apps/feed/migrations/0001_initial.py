# Generated by Django 4.0.4 on 2022-12-06 11:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import console_api.apps.models.abstract


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('source', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParsingRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', console_api.apps.models.abstract.CreationDateTimeField(auto_now_add=True, verbose_name='создано')),
                ('modified', console_api.apps.models.abstract.ModificationDateTimeField(auto_now=True, verbose_name='изменено')),
            ],
            options={
                'verbose_name': 'Правило парсинга',
                'verbose_name_plural': 'Правила парсинга',
            },
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', console_api.apps.models.abstract.CreationDateTimeField(auto_now_add=True, verbose_name='создано')),
                ('modified', console_api.apps.models.abstract.ModificationDateTimeField(auto_now=True, verbose_name='изменено')),
                ('type_of_feed', models.CharField(choices=[('EMAIL_FROM', 'FEMA'), ('EMAIL_SUBJECT', 'SEMA'), ('MD5_HASH', 'MD5H'), ('SHA1_HASH', 'SHA1'), ('SHA256_HASH', 'SHA2'), ('IP', 'IPAD'), ('URL', 'URLS'), ('DOMAIN', 'DOMN'), ('FILENAME', 'FILE'), ('REGISTRY', 'REGS')], default='IPAD', max_length=13, verbose_name='Тип фида')),
                ('format_of_feed', models.CharField(choices=[('CSV_FILE', 'CSV'), ('JSON_FILE', 'JSON'), ('XML_FILE', 'XML'), ('TXT_FILE', 'TXT')], default='TXT', max_length=15, verbose_name='Формат фида')),
                ('auth_type', models.CharField(choices=[('NO_AUTH', 'NAU'), ('API', 'API'), ('BASIC', 'BSC')], default='NAU', max_length=7, verbose_name='Тип авторизации')),
                ('polling_frequency', models.CharField(choices=[('NEVER', 'NVR'), ('THIRTY_MINUTES', 'M30'), ('ONE_HOUR', 'HR1'), ('TWO_HOURS', 'HR2'), ('FOUR_HOURS', 'HR4'), ('EIGHT_HOURS', 'HR8'), ('SIXTEEN_HOURS', 'H16'), ('TWENTY_FOUR_HOURS', 'H24')], default='NVR', max_length=17, verbose_name='Частота обновления фида')),
                ('auth_login', models.CharField(blank=True, max_length=32, null=True, verbose_name='Логин для авторизации')),
                ('auth_password', models.CharField(blank=True, max_length=64, null=True, verbose_name='Пароль для авторизации')),
                ('auth_querystring', models.CharField(blank=True, max_length=128, null=True, verbose_name='Строка для авторизации')),
                ('separator', models.CharField(blank=True, max_length=8, null=True, verbose_name='Разделитель для CSV формата')),
                ('custom_field', models.CharField(blank=True, max_length=128, null=True, verbose_name='Кастомное поле')),
                ('sertificate', models.FileField(blank=True, null=True, upload_to='', verbose_name='Файл сертификат')),
                ('vendor', models.CharField(max_length=32, verbose_name='Вендор')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Название фида')),
                ('link', models.CharField(max_length=255, verbose_name='Ссылка на фид')),
                ('confidence', models.IntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='Достоверность')),
                ('records_quantity', models.IntegerField(blank=True, null=True, verbose_name='Количество записей')),
                ('update_status', models.CharField(choices=[('ENABLED', 'ENABLED'), ('DISABLED', 'DISABLED'), ('UPDATE_ERROR', 'UPDATE_ERROR')], default='ENABLED', max_length=15)),
                ('ts', models.DateTimeField(auto_now_add=True)),
                ('indicators', models.ManyToManyField(blank=True, related_name='feeds', to='indicator.indicator', verbose_name='Индикатор')),
                ('parsing_rules', models.ManyToManyField(blank=True, related_name='feed_parsing_rules', to='feed.parsingrule', verbose_name='Правила для парсинга')),
                ('source', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='source.source')),
            ],
            options={
                'verbose_name': 'Фид',
                'verbose_name_plural': 'Фиды',
            },
        ),
    ]
