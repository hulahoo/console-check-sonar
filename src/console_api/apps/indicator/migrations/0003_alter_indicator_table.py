# Generated by Django 4.0.4 on 2022-12-14 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicator', '0002_alter_indicator_type'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='indicator',
            table='sessions',
        ),
    ]