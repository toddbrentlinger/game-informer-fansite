# Generated by Django 4.0.1 on 2022-07-18 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('people', '0001_initial'),
        ('replay', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='thumbnail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='replay.thumbnail'),
        ),
    ]
