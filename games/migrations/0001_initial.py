# Generated by Django 4.0.1 on 2022-08-19 02:11

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
                ('id', models.PositiveIntegerField(help_text='Enter IGDB ID of the item.', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Enter name of the item.', max_length=200)),
                ('slug', models.SlugField(help_text='Enter a url-safe, unique, lower-case version of the item.', max_length=200, unique=True)),
                ('url', models.URLField(blank=True, help_text='Enter the IGDB website address (URL) of the item.')),
                ('country', models.PositiveSmallIntegerField(blank=True, help_text='Enter the ISO 3166-1 country code.', null=True)),
                ('description', models.TextField(blank=True, help_text='Enter free text description of the company.')),
                ('start_date', models.DateTimeField(blank=True, help_text='Enter date the company was founded.', null=True, verbose_name='Release Date')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.PositiveIntegerField(help_text='Enter IGDB ID of the item.', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Enter name of the item.', max_length=200)),
                ('slug', models.SlugField(help_text='Enter a url-safe, unique, lower-case version of the item.', max_length=200, unique=True)),
                ('url', models.URLField(blank=True, help_text='Enter the IGDB website address (URL) of the item.')),
                ('summary', models.TextField(blank=True, help_text='Enter description of the game.')),
                ('storyline', models.TextField(blank=True, help_text="Enter short description of the game's story.")),
                ('release_date', models.DateTimeField(blank=True, help_text='Enter date the game was released.', null=True, verbose_name='Release Date')),
            ],
            options={
                'ordering': ['name', 'release_date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.PositiveIntegerField(help_text='Enter IGDB ID of the item.', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Enter name of the item.', max_length=200)),
                ('slug', models.SlugField(help_text='Enter a url-safe, unique, lower-case version of the item.', max_length=200, unique=True)),
                ('url', models.URLField(blank=True, help_text='Enter the IGDB website address (URL) of the item.')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ImageIGDB',
            fields=[
                ('id', models.PositiveIntegerField(help_text='Enter IGDB ID of the image.', primary_key=True, serialize=False)),
                ('image_id', models.CharField(help_text='Enter the ID of the image used to construct an IGDB image link.', max_length=100)),
                ('width', models.PositiveSmallIntegerField(blank=True, help_text='Enter the width of the image in pixels.', null=True)),
                ('height', models.PositiveSmallIntegerField(blank=True, help_text='Enter the height of the image in pixels.', null=True)),
            ],
            options={
                'verbose_name': 'Image',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.PositiveIntegerField(help_text='Enter IGDB ID of the item.', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Enter name of the item.', max_length=200)),
                ('slug', models.SlugField(help_text='Enter a url-safe, unique, lower-case version of the item.', max_length=200, unique=True)),
                ('url', models.URLField(blank=True, help_text='Enter the IGDB website address (URL) of the item.')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.PositiveIntegerField(help_text='Enter IGDB ID of the item.', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Enter name of the item.', max_length=200)),
                ('slug', models.SlugField(help_text='Enter a url-safe, unique, lower-case version of the item.', max_length=200, unique=True)),
                ('url', models.URLField(blank=True, help_text='Enter the IGDB website address (URL) of the item.')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.PositiveSmallIntegerField(choices=[(1, 'Official'), (2, 'Wikia'), (3, 'Wikipedia'), (4, 'Facebook'), (5, 'Twitter'), (6, 'Twitch'), (8, 'Instagram'), (9, 'Youtube'), (10, 'Iphone'), (11, 'Ipad'), (12, 'Android'), (13, 'Steam'), (14, 'Reddit'), (15, 'Itch'), (16, 'Epicgames'), (17, 'Gog'), (18, 'Discord')])),
                ('trusted', models.BooleanField(default=False)),
                ('url', models.URLField(help_text='Enter the IGDB website address (URL) of the item.')),
            ],
        ),
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(help_text='Enter the game.', on_delete=django.db.models.deletion.CASCADE, to='games.game')),
                ('image', models.OneToOneField(help_text='Enter the IGDB Image.', on_delete=django.db.models.deletion.CASCADE, to='games.imageigdb')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.PositiveIntegerField(help_text='Enter IGDB ID of the item.', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Enter name of the item.', max_length=200)),
                ('slug', models.SlugField(help_text='Enter a url-safe, unique, lower-case version of the item.', max_length=200, unique=True)),
                ('url', models.URLField(blank=True, help_text='Enter the IGDB website address (URL) of the item.')),
                ('abbreviation', models.CharField(blank=True, help_text='Enter shortened abbreviation for the system/platform.', max_length=20)),
                ('alternative_name', models.CharField(blank=True, help_text='Enter alternative names as list separated by commas.', max_length=1000)),
                ('generation', models.PositiveSmallIntegerField(blank=True, help_text='Enter the generation of the system/platform.', null=True)),
                ('summary', models.TextField(blank=True, help_text='Enter a summary of the first Version of the platform.')),
                ('logo', models.ForeignKey(blank=True, help_text='Enter logo of the first Version of the platform.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='games.imageigdb')),
                ('websites', models.ManyToManyField(blank=True, help_text='Enter websites associated with the system/platform.', to='games.Website')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GameVideo',
            fields=[
                ('id', models.PositiveIntegerField(help_text='Enter IGDB ID of the video.', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, help_text='Enter the name of the video.', max_length=200)),
                ('video_id', models.CharField(help_text='Enter the external ID of the video (usually YouTube).', max_length=50)),
                ('game', models.ForeignKey(help_text='Enter the game.', on_delete=django.db.models.deletion.CASCADE, to='games.game')),
            ],
            options={
                'verbose_name': 'Video',
            },
        ),
        migrations.AddField(
            model_name='game',
            name='cover',
            field=models.OneToOneField(blank=True, help_text='Enter the cover of the game.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='games.imageigdb'),
        ),
        migrations.AddField(
            model_name='game',
            name='developers',
            field=models.ManyToManyField(blank=True, help_text='Enter developers of the game.', to='games.Developer'),
        ),
        migrations.AddField(
            model_name='game',
            name='genres',
            field=models.ManyToManyField(blank=True, help_text='Enter genres of the game.', to='games.Genre'),
        ),
        migrations.AddField(
            model_name='game',
            name='keywords',
            field=models.ManyToManyField(blank=True, help_text='Enter keywords of the game.', to='games.Keyword'),
        ),
        migrations.AddField(
            model_name='game',
            name='platforms',
            field=models.ManyToManyField(blank=True, help_text='Enter game platforms (ex. PC, PS4, XBox 360, etc.).', to='games.Platform'),
        ),
        migrations.AddField(
            model_name='game',
            name='themes',
            field=models.ManyToManyField(blank=True, help_text='Enter themes of the game.', to='games.Theme'),
        ),
        migrations.AddField(
            model_name='game',
            name='websites',
            field=models.ManyToManyField(blank=True, help_text='Enter websites associated with the game.', to='games.Website'),
        ),
        migrations.CreateModel(
            name='Franchise',
            fields=[
                ('id', models.PositiveIntegerField(help_text='Enter IGDB ID of the item.', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Enter name of the item.', max_length=200)),
                ('slug', models.SlugField(help_text='Enter a url-safe, unique, lower-case version of the item.', max_length=200, unique=True)),
                ('url', models.URLField(blank=True, help_text='Enter the IGDB website address (URL) of the item.')),
                ('games', models.ManyToManyField(help_text='Enter games associated with the item.', to='games.Game')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='developer',
            name='logo',
            field=models.ForeignKey(blank=True, help_text='Enter logo of the company.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='games.imageigdb'),
        ),
        migrations.AddField(
            model_name='developer',
            name='websites',
            field=models.ManyToManyField(blank=True, help_text='Enter companies official websites.', to='games.Website'),
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.PositiveIntegerField(help_text='Enter IGDB ID of the item.', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Enter name of the item.', max_length=200)),
                ('slug', models.SlugField(help_text='Enter a url-safe, unique, lower-case version of the item.', max_length=200, unique=True)),
                ('url', models.URLField(blank=True, help_text='Enter the IGDB website address (URL) of the item.')),
                ('games', models.ManyToManyField(help_text='Enter games associated with the item.', to='games.Game')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Artwork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(help_text='Enter the game.', on_delete=django.db.models.deletion.CASCADE, to='games.game')),
                ('image', models.OneToOneField(help_text='Enter the IGDB Image.', on_delete=django.db.models.deletion.CASCADE, to='games.imageigdb')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
