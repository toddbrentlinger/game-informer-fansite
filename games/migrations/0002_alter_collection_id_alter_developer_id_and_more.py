# Generated by Django 4.0.1 on 2022-07-18 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='id',
            field=models.PositiveIntegerField(help_text='Enter IGDB ID of the item.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='developer',
            name='id',
            field=models.PositiveIntegerField(help_text='Enter IGDB ID of the item.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='franchise',
            name='id',
            field=models.PositiveIntegerField(help_text='Enter IGDB ID of the item.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='game',
            name='id',
            field=models.PositiveIntegerField(help_text='Enter IGDB ID of the item.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='genre',
            name='id',
            field=models.PositiveIntegerField(help_text='Enter IGDB ID of the item.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='id',
            field=models.PositiveIntegerField(help_text='Enter IGDB ID of the item.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='platform',
            name='id',
            field=models.PositiveIntegerField(help_text='Enter IGDB ID of the item.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='theme',
            name='id',
            field=models.PositiveIntegerField(help_text='Enter IGDB ID of the item.', primary_key=True, serialize=False),
        ),
    ]