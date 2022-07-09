# Generated by Django 4.0.1 on 2022-07-08 23:50

from django.db import migrations
from utilities.data_migration import initialize_database

class Migration(migrations.Migration):

    dependencies = [
        ('fansite', '0002_initial'),
        ('games', '0001_initial'),
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initialize_database),
    ]
