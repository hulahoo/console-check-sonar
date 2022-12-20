# Generated by Django 4.0.4 on 2022-12-19 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feed',
            old_name='sertificate',
            new_name='certificate',
        ),
        migrations.RenameField(
            model_name='feed',
            old_name='format_of_feed',
            new_name='format',
        ),
        migrations.RemoveField(
            model_name='feed',
            name='name',
        ),
        migrations.AddField(
            model_name='feed',
            name='title',
            field=models.CharField(default='test', max_length=255, unique=True, verbose_name='Название фида'),
            preserve_default=False,
        ),
    ]
