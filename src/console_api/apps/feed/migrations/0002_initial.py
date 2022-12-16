# Generated by Django 4.0.4 on 2022-12-16 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('feed', '0001_initial'),
        ('source', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL("CREATE TABLE IF NOT EXISTS 'indicator_feed_relationships' ('id' SERIAL NOT NULL PRIMARY KEY, 'created_at' TIMESTAMP NOT NULL, 'deleted_at' TIMESTAMP NOT NULL, 'feed_id' INTEGER REFERENCES feed(id), 'indicator_id' INTEGER REFERENCES indicators(id)"),
        migrations.AddField(
            model_name='feed',
            name='parsing_rules',
            field=models.ManyToManyField(blank=True, related_name='feed_parsing_rules', to='feed.parsingrule', verbose_name='Правила для парсинга'),
        ),
        migrations.AddField(
            model_name='feed',
            name='source',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='source.source'),
        ),
    ]
