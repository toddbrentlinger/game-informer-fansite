# Generated by Django 4.0.1 on 2022-03-20 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_alter_game_release_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='release_date',
            field=models.DateTimeField(blank=True, help_text='Enter date the game was released.', null=True, verbose_name='Release Date'),
        ),
    ]