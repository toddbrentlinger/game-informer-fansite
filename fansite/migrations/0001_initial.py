# Generated by Django 4.0.1 on 2022-07-18 01:31

from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension, UnaccentExtension
from utilities.data_migration import initialize_database

class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_alter_collection_id_alter_developer_id_and_more'),
        ('people', '0002_initial'),
        ('replay', '0001_initial'),
    ]

    operations = [
        TrigramExtension(),
        UnaccentExtension(),
        migrations.RunPython(initialize_database),
    ]
