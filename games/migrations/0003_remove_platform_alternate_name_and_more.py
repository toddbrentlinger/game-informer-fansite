# Generated by Django 4.0.1 on 2022-06-27 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_alter_game_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='platform',
            name='alternate_name',
        ),
        migrations.AddField(
            model_name='platform',
            name='alternative_name',
            field=models.CharField(blank=True, help_text='Enter alternative names as list separated by commas.', max_length=1000),
        ),
    ]