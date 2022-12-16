# Generated by Django 4.0.4 on 2022-12-16 16:54

import console_api.apps.models.abstract
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', console_api.apps.models.abstract.CreationDateTimeField(auto_now_add=True, verbose_name='создано')),
                ('updated_at', console_api.apps.models.abstract.ModificationDateTimeField(auto_now=True, verbose_name='изменено')),
                ('title', models.CharField(max_length=30, verbose_name='Название тега')),
                ('weight', models.IntegerField(blank=True, max_length=10, null=True, verbose_name='Вес тега')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'db_table': 'tags',
            },
        ),
    ]
