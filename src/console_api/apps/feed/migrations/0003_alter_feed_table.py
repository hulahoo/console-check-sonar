# Generated by Django 4.0.4 on 2022-12-13 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_alter_feed_auth_type_alter_feed_format_of_feed_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='feed',
            table='feeds',
        ),
    ]
