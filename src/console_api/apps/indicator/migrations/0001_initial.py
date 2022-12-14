# Generated by Django 4.0.4 on 2022-12-06 11:55

import django.core.validators
from django.db import migrations, models
import apps.common.enums
import apps.models.abstract


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tag', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', apps.models.abstract.CreationDateTimeField(auto_now_add=True, verbose_name='создано')),
                ('modified', apps.models.abstract.ModificationDateTimeField(auto_now=True, verbose_name='изменено')),
                ('type', models.CharField(choices=[('EMAIL_FROM', 'FEMA'), ('EMAIL_SUBJECT', 'SEMA'), ('MD5_HASH', 'MD5H'), ('SHA1_HASH', 'SHA1'), ('SHA256_HASH', 'SHA2'), ('IP', 'IPAD'), ('URL', 'URLS'), ('DOMAIN', 'DOMN'), ('FILENAME', 'FILE'), ('REGISTRY', 'REGS')], default=apps.common.enums.TypesEnum['IP'], max_length=13, verbose_name='Тип индикатора')),
                ('uuid', models.CharField(max_length=255, unique=True, verbose_name='Уникальный идентификатор индикатора')),
                ('category', models.CharField(blank=True, max_length=128, null=True, verbose_name='Категория индикатора')),
                ('value', models.CharField(max_length=256, verbose_name='Значение индикатора')),
                ('weight', models.IntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='Вес')),
                ('false_detected', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='счетчик ложных срабатываний')),
                ('positive_detected', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='счетчик позитивных срабатываний')),
                ('detected', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='общий счетчик срабатываний')),
                ('first_detected_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата первого срабатывания')),
                ('last_detected_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата последнего срабатывания')),
                ('supplier_name', models.CharField(max_length=128, verbose_name='Название источника')),
                ('supplier_vendor_name', models.CharField(max_length=128, verbose_name='Название поставщика ')),
                ('supplier_type', models.CharField(max_length=64, verbose_name='Тип поставщика')),
                ('supplier_confidence', models.IntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='Достоверность')),
                ('supplier_created_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата последнего обновления')),
                ('ioc_context_exploits_md5', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_exploits_sha1', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_exploits_sha256', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_exploits_threat', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_av_verdict', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_md5', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_sha1', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_sha256', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_affected_products_product', models.CharField(blank=True, max_length=64, null=True)),
                ('joc_context_domains', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_file_names', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_file_size', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_file_type', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_files_behaviour', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_files_md5', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_files_sha1', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_files_sha256', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_files_threat', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_malware', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_mask', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_popularity', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_port', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_protocol', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_publication_name', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_severity', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_type', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_url', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_urls_url', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_vendors_vendor', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_geo', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_id', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_industry', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_ip', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_ip_geo', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_ip_whois_asn', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_ip_whois_contact_abuse_country', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_ip_whois_contact_abuse_email', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_ip_whois_contact_abuse_name', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_ip_whois_contact_owner_city', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_ip_whois_contact_owner_code', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_ip_whois_contact_owner_country', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_ip_whois_contact_owner_email', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_ip_whois_contact_owner_name', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_ip_whois_country', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_ip_whois_created', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_ip_whois_desrc', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_ip_whois_net_name', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_ip_whois_net_range', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_ip_whois_updated', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_whois_mx', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_whois_mx_ips', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_whois_ns', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_whois_ns_ips', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_whois_city', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_whois_country', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_whois_created', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_whois_domain', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_whois_email', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_whois_expires', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_whois_name', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_whois_org', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_whois_registrar_email', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_whois_registrar_name', models.CharField(blank=True, max_length=64, null=True)),
                ('ioc_context_whois_updated', models.CharField(blank=True, max_length=64, null=True)),
                ('ttl', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Дата удаления')),
                ('tag', models.ManyToManyField(related_name='tags', to='tag.tag')),
            ],
            options={
                'verbose_name': 'Индикатор',
                'verbose_name_plural': 'Индикаторы',
            },
        ),
    ]
