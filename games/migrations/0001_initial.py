# Generated by Django 4.0.1 on 2022-03-06 21:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.PositiveSmallIntegerField(help_text='Enter IGDB ID for this genre.', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Enter name of this genre.', max_length=200)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PlatformLogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Platform Logo',
            },
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.PositiveSmallIntegerField(help_text='Enter IGDB ID for this system/platform.', primary_key=True, serialize=False)),
                ('abbreviation', models.CharField(help_text='Enter shortened abbreviation for this system/platform.', max_length=20)),
                ('alternate_name', models.CharField(help_text='Enter alternate names as list separated by commas.', max_length=1000)),
                ('name', models.CharField(help_text='Enter name of this system/platform.', max_length=200)),
                ('logo', models.ForeignKey(blank=True, help_text='Enter logo for this system/platform.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='games.platformlogo')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('igdb_id', models.PositiveIntegerField(blank=True, help_text='Enter IGDB game ID to be used with API. If ID entered, other fields do NOT need to be filled out.', null=True, verbose_name='IGDB ID')),
                ('name', models.CharField(help_text='Enter game title.', max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('summary', models.TextField(blank=True, help_text='Enter summary of the game.')),
                ('release_date', models.DateField(help_text='Enter date the game was released.', verbose_name='Release Date')),
                ('developer', models.ForeignKey(blank=True, help_text='Enter developer of the game.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='games.developer')),
                ('genre', models.ManyToManyField(blank=True, help_text='Enter genres of the game.', to='games.Genre')),
                ('platform', models.ForeignKey(blank=True, help_text='Enter game platform (ex. PC, PS4, XBox 360, etc.).', null=True, on_delete=django.db.models.deletion.SET_NULL, to='games.platform')),
            ],
            options={
                'ordering': ['name', 'release_date'],
            },
        ),
    ]