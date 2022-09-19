# Generated by Django 4.0.1 on 2022-09-19 01:40

from django.db import migrations
from utilities.replay_data_migration import initialize_database as replay_init

class Migration(migrations.Migration):

    dependencies = [
        ('fansite', '0001_initial'),
        ('episodes', '0002_initial'),
        ('games', '0001_initial'),
        ('people', '0001_initial'),
        ('replay', '0001_initial'),
        ('shows', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(replay_init),
    ]
