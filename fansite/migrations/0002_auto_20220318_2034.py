# Generated by Django 4.0.1 on 2022-03-19 03:34

from django.db import migrations
from fansite.other_scripts.data_migration import initialize_database

class Migration(migrations.Migration):

    dependencies = [
        ('fansite', '0001_initial'),
        # added dependency to enable models from 'game' app to initialize_database method
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initialize_database),
    ]
