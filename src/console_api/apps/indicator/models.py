import uuid as uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.tag.models import Tag
from apps.common.enums import TypesEnum
from apps.models.abstract import BaseModel


class Indicator(BaseModel):
    """
    Модель индикатора.
    """
    uuid = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(
        "Тип индикатора", max_length=13, default=TypesEnum.IP.value
    )
    category = models.CharField(
        "Категория индикатора", max_length=128, blank=True, null=True
    )
    value = models.CharField("Значение индикатора", max_length=256)
    weight = models.IntegerField(
        "Вес", validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    tag = models.ManyToManyField(Tag, blank=True, null=True)
    false_detected = models.IntegerField(
        "счетчик ложных срабатываний", validators=[MinValueValidator(0)], default=0
    )
    positive_detected = models.IntegerField(
        "счетчик позитивных срабатываний", validators=[MinValueValidator(0)], default=0
    )
    detected = models.IntegerField(
        "общий счетчик срабатываний", validators=[MinValueValidator(0)], default=0
    )
    first_detected_date = models.DateTimeField(
        "Дата первого срабатывания", blank=True, null=True
    )
    last_detected_date = models.DateTimeField(
        "Дата последнего срабатывания", blank=True, null=True
    )
    # Данные об источнике
    supplier_name = models.CharField("Название источника", max_length=128)
    supplier_vendor_name = models.CharField("Название поставщика ", max_length=128)
    supplier_type = models.CharField("Тип поставщика", max_length=64)
    supplier_confidence = models.IntegerField(
        "Достоверность", validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    supplier_created_date = models.DateTimeField(
        "Дата последнего обновления", blank=True, null=True
    )
    # Контекст
    ioc_context_exploits_md5 = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_exploits_sha1 = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_exploits_sha256 = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_exploits_threat = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_av_verdict = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_ip = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_md5 = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_sha1 = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_sha256 = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_affected_products_product = models.CharField(
        max_length=64, blank=True, null=True
    )
    joc_context_domains = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_file_names = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_file_size = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_file_type = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_files_behaviour = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_files_md5 = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_files_sha1 = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_files_sha256 = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_files_threat = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_malware = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_mask = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_popularity = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_port = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_protocol = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_publication_name = models.CharField(
        max_length=64, blank=True, null=True
    )
    ioc_context_severity = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_type = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_url = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_urls_url = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_vendors_vendor = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_geo = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_id = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_industry = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_ip = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_ip_geo = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_ip_whois_asn = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_ip_whois_contact_abuse_country = models.CharField(
        max_length=64, blank=True, null=True
    )
    ioc_context_ip_whois_contact_abuse_email = models.CharField(
        max_length=64, blank=True, null=True
    )
    ioc_context_ip_whois_contact_abuse_name = models.CharField(
        max_length=64, blank=True, null=True
    )
    ioc_context_ip_whois_contact_owner_city = models.CharField(
        max_length=64, blank=True, null=True
    )
    ioc_context_ip_whois_contact_owner_code = models.CharField(
        max_length=64, blank=True, null=True
    )
    ioc_context_ip_whois_contact_owner_country = models.CharField(
        max_length=64, blank=True, null=True
    )
    ioc_context_ip_whois_contact_owner_email = models.CharField(
        max_length=64, blank=True, null=True
    )
    ioc_context_ip_whois_contact_owner_name = models.CharField(
        max_length=64, blank=True, null=True
    )
    ioc_context_ip_whois_country = models.CharField(
        max_length=64, blank=True, null=True
    )
    ioc_context_ip_whois_created = models.CharField(
        max_length=64, blank=True, null=True
    )
    ioc_context_ip_whois_desrc = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_ip_whois_net_name = models.CharField(
        max_length=64, blank=True, null=True
    )
    ioc_context_ip_whois_net_range = models.CharField(
        max_length=64, blank=True, null=True
    )
    ioc_context_ip_whois_updated = models.CharField(
        max_length=64, blank=True, null=True
    )
    ioc_context_whois_mx = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_whois_mx_ips = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_whois_ns = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_whois_ns_ips = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_whois_city = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_whois_country = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_whois_created = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_whois_domain = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_whois_email = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_whois_expires = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_whois_name = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_whois_org = models.CharField(max_length=64, blank=True, null=True)
    ioc_context_whois_registrar_email = models.CharField(
        max_length=64, blank=True, null=True
    )
    ioc_context_whois_registrar_name = models.CharField(
        max_length=64, blank=True, null=True
    )
    ioc_context_whois_updated = models.CharField(max_length=64, blank=True, null=True)

    # время жизни
    ttl = models.DateTimeField("Дата удаления", blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.value}"

    # @classmethod
    # def get_model_fields(cls):
    #     return {i.attname: list(i.class_lookups.keys()) for i in cls._meta.fields}

    class Meta:
        verbose_name = "Индикатор"
        verbose_name_plural = "Индикаторы"
        db_table = "sessions"


class IndicatorActivities(BaseModel):
    """
    Модель Активность по Индикатору
    """
    ACTIVITIES_TYPE = (
        ("add_comment", "add-comment"),
        ("add_tag", "add-tag"),
        ("remove_tag", "remove-tag"),
        ("move_to_archive", "move-to-archive"),
        ("move_from_archive", "move-from-archive"),
    )
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, verbose_name='Активность по индикатору',
                                  related_name='activities')
    type = models.CharField(max_length=50, choices=ACTIVITIES_TYPE, verbose_name='Тип')
    details = models.JSONField()

    class Meta:
        verbose_name = "Активность по Индикатору"
        verbose_name_plural = "Активности по Индикатору"
        db_table = "activities"

