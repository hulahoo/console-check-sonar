# Generated by Django 4.0.4 on 2022-12-20 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicator', '0002_remove_indicator_ioc_context_affected_products_product_and_more'),
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='indicators',
            field=models.ManyToManyField(blank=True, null=True, to='indicator.indicator'),
        ),
    ]
