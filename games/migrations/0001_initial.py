# Generated by Django 4.0.1 on 2022-07-04 23:07

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
                ('id', models.PositiveIntegerField(help_text='Enter IGDB ID of the company.', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Enter name of the company.', max_length=200)),
                ('country', models.PositiveSmallIntegerField(blank=True, help_text='Enter the ISO 3166-1 country code.', null=True)),
                ('description', models.TextField(blank=True, help_text='Enter free text description of the company.')),
                ('slug', models.SlugField(help_text='Enter a url-safe, unique, lower-case version of the company.', max_length=200, unique=True)),
                ('url', models.URLField(help_text='Enter the IGDB website address (URL) of the company.')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('igdb_id', models.PositiveIntegerField(blank=True, help_text='Enter IGDB game ID to be used with API. If ID entered, other fields do NOT need to be filled out.', null=True, verbose_name='IGDB ID')),
                ('name', models.CharField(help_text='Enter game title.', max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('summary', models.TextField(blank=True, help_text='Enter description of the game.')),
                ('storyline', models.TextField(blank=True, help_text="Enter short description of the game's story.")),
                ('release_date', models.DateTimeField(blank=True, help_text='Enter date the game was released.', null=True, verbose_name='Release Date')),
                ('url', models.URLField(blank=True, help_text='Enter the IGDB website address (URL) of the game.')),
            ],
            options={
                'ordering': ['name', 'release_date'],
            },
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
            name='ImageIGDB',
            fields=[
                ('id', models.PositiveIntegerField(help_text='Enter IGDB ID of the image.', primary_key=True, serialize=False)),
                ('image_id', models.CharField(help_text='Enter the ID of the image used to construct an IGDB image link.', max_length=100)),
                ('width', models.PositiveSmallIntegerField(help_text='Enter the width of the image in pixels.')),
                ('height', models.PositiveSmallIntegerField(help_text='Enter the height of the image in pixels.')),
            ],
            options={
                'verbose_name': 'Image',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(help_text='Enter the game of the screenshot.', on_delete=django.db.models.deletion.CASCADE, to='games.game')),
                ('image', models.OneToOneField(help_text='Enter the IGDB Image for the screenshot.', on_delete=django.db.models.deletion.CASCADE, to='games.imageigdb')),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.PositiveSmallIntegerField(help_text='Enter IGDB ID of the system/platform.', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Enter name of this system/platform.', max_length=200)),
                ('abbreviation', models.CharField(blank=True, help_text='Enter shortened abbreviation for this system/platform.', max_length=20)),
                ('alternative_name', models.CharField(blank=True, help_text='Enter alternative names as list separated by commas.', max_length=1000)),
                ('slug', models.SlugField(help_text='Enter a url-safe, unique, lower-case version of the platform.', max_length=200, unique=True)),
                ('summary', models.TextField(blank=True, help_text='Enter a summary of the first Version of this platform.')),
                ('url', models.URLField(help_text='Enter the IGDB website address (URL) of the platform.')),
                ('logo', models.ForeignKey(blank=True, help_text='Enter logo of the first Version of this platform.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='games.imageigdb')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='game',
            name='cover',
            field=models.OneToOneField(blank=True, help_text='Enter the cover of the game.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='games.imageigdb'),
        ),
        migrations.AddField(
            model_name='game',
            name='developer',
            field=models.ForeignKey(blank=True, help_text='Enter developer of the game.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='games.developer'),
        ),
        migrations.AddField(
            model_name='game',
            name='genres',
            field=models.ManyToManyField(blank=True, help_text='Enter genres of the game.', to='games.Genre'),
        ),
        migrations.AddField(
            model_name='game',
            name='platform',
            field=models.ForeignKey(blank=True, help_text='Enter game platform (ex. PC, PS4, XBox 360, etc.).', null=True, on_delete=django.db.models.deletion.SET_NULL, to='games.platform'),
        ),
        migrations.AddField(
            model_name='developer',
            name='logo',
            field=models.ForeignKey(blank=True, help_text='Enter logo of the company.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='games.imageigdb'),
        ),
    ]
