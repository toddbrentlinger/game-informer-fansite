# Generated by Django 4.0.1 on 2022-03-01 19:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter article title.', max_length=100)),
                ('datetime', models.DateTimeField(help_text='Enter date and time article was published.')),
                ('content', models.TextField(help_text='Enter main content of article.')),
                ('url', models.URLField(help_text='Enter URL of article.', null=True, verbose_name='URL')),
            ],
            options={
                'ordering': ['-datetime'],
            },
        ),
        migrations.CreateModel(
            name='ExternalLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(help_text='Enter URL of external link.', verbose_name='URL')),
                ('title', models.CharField(help_text='Enter display title of external link.', max_length=100)),
            ],
            options={
                'verbose_name': 'External Link',
            },
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Enter first name.', max_length=100, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, help_text='Enter last name.', max_length=100, verbose_name='Last Name')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Heading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter heading title.', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ReplaySeason',
            fields=[
                ('number', models.SmallIntegerField(help_text='Enter unique number of Replay season.', primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, help_text='Enter description for the Replay season.')),
            ],
            options={
                'verbose_name': 'Replay Season',
                'ordering': ['-number'],
            },
        ),
        migrations.CreateModel(
            name='SegmentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter title of segment.', max_length=100)),
                ('abbreviation', models.CharField(blank=True, help_text='Enter shortened abbreviation of segment title.', max_length=10)),
                ('description', models.CharField(blank=True, help_text='Enter description of segment.', max_length=1000)),
            ],
            options={
                'verbose_name': 'Segment Type',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Enter first name.', max_length=100, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, help_text='Enter last name.', max_length=100, verbose_name='Last Name')),
            ],
            options={
                'verbose_name': 'Staff Member',
                'verbose_name_plural': 'Staff',
                'ordering': ['last_name', 'first_name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StaffPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter title of position.', max_length=200)),
            ],
            options={
                'verbose_name': 'Staff Position',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='SuperReplay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Super Replay',
            },
        ),
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quality', models.CharField(choices=[('DEFAULT', 'Default'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('STANDARD', 'Standard'), ('MAXRES', 'Maxres')], help_text='Enter quality of thumbnail.', max_length=20)),
                ('url', models.URLField(help_text='Enter URL of thumbnail.', verbose_name='URL')),
                ('width', models.PositiveSmallIntegerField(help_text='Enter width of thumbnail')),
                ('height', models.PositiveSmallIntegerField(help_text='Enter height of thumbnail')),
            ],
        ),
        migrations.CreateModel(
            name='YouTubeVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('youtube_id', models.CharField(blank=True, help_text='Enter YouTube video ID', max_length=15, verbose_name='Video ID')),
                ('title', models.CharField(help_text='Enter title of the video.', max_length=100)),
                ('views', models.PositiveBigIntegerField(blank=True, help_text='Enter number of views.', null=True)),
                ('likes', models.PositiveIntegerField(blank=True, help_text='Enter number of likes.', null=True)),
                ('dislikes', models.PositiveIntegerField(blank=True, help_text='Enter the number of dislikes.', null=True)),
                ('thumbnails', models.ManyToManyField(help_text='Enter thumbnail images for the video.', to='fansite.Thumbnail')),
            ],
            options={
                'verbose_name': 'YouTube Video',
            },
        ),
        migrations.CreateModel(
            name='SuperReplayEpisode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(help_text='Enter episode title.', max_length=100, unique=True)),
                ('runtime', models.CharField(blank=True, help_text='Enter episode runtime in format hh:mm:ss.', max_length=10)),
                ('airdate', models.DateField(help_text='Enter original date the episode first aired.')),
                ('headings', models.JSONField(blank=True, help_text='Enter JSON of different headings with key being the heading title and value being the content.', null=True)),
                ('external_links', models.ManyToManyField(blank=True, help_text='Enter any external URL links (NOT including Game Informer article OR YouTube video).', to='fansite.ExternalLink', verbose_name='External Links')),
                ('featuring', models.ManyToManyField(blank=True, help_text='Enter staff members who feature in the episode (NOT including the host).', related_name='%(app_label)s_%(class)s_featuring_related', related_query_name='%(app_label)s_%(class)ss_featuring', to='fansite.Staff')),
                ('guests', models.ManyToManyField(blank=True, help_text='Enter any other guests (NOT official staff members).', to='fansite.Guest')),
                ('host', models.ForeignKey(blank=True, help_text='Enter staff member who hosts the episode.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_host_related', related_query_name='%(app_label)s_%(class)ss_host', to='fansite.staff')),
                ('super_replay', models.ForeignKey(help_text='Enter Super Replay for this episode.', on_delete=django.db.models.deletion.CASCADE, to='fansite.superreplay')),
                ('thumbnails', models.ManyToManyField(blank=True, help_text='Enter thumbnail images for the episode.', to='fansite.Thumbnail')),
                ('youtube_video', models.OneToOneField(blank=True, help_text='Enter the YouTube video for the episode.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='fansite.youtubevideo', verbose_name='YouTube Video')),
            ],
            options={
                'verbose_name': 'Super Replay Episode',
                'ordering': ['airdate'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StaffPositionInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_year', models.PositiveSmallIntegerField(help_text='Enter date started the position.', verbose_name='Start Year')),
                ('end_year', models.PositiveSmallIntegerField(blank=True, help_text='Enter date started the position.', null=True, verbose_name='End Year')),
                ('position', models.ForeignKey(help_text='Enter position of the staff member.', on_delete=django.db.models.deletion.PROTECT, to='fansite.staffposition')),
                ('staff', models.ForeignKey(help_text='Enter staff member for this position instance.', on_delete=django.db.models.deletion.CASCADE, to='fansite.staff')),
            ],
            options={
                'verbose_name': 'Staff Position Instance',
                'ordering': ['-start_year'],
            },
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique ID for this particular segment instance.', primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, help_text='Enter description of this segment instance.')),
                ('games', models.ManyToManyField(blank=True, help_text='Enter games played during the segment.', to='game.Game')),
                ('type', models.ForeignKey(help_text='Enter type of segment.', on_delete=django.db.models.deletion.PROTECT, to='fansite.segmenttype')),
            ],
        ),
        migrations.CreateModel(
            name='ReplayEpisode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(help_text='Enter episode title.', max_length=100, unique=True)),
                ('runtime', models.CharField(blank=True, help_text='Enter episode runtime in format hh:mm:ss.', max_length=10)),
                ('airdate', models.DateField(help_text='Enter original date the episode first aired.')),
                ('headings', models.JSONField(blank=True, help_text='Enter JSON of different headings with key being the heading title and value being the content.', null=True)),
                ('number', models.SmallIntegerField(help_text='Enter Replay episode number (unofficial episodes use negative numbers).', unique=True)),
                ('article', models.OneToOneField(blank=True, help_text='Enter article for the Replay episode.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='fansite.article')),
                ('external_links', models.ManyToManyField(blank=True, help_text='Enter any external URL links (NOT including Game Informer article OR YouTube video).', to='fansite.ExternalLink', verbose_name='External Links')),
                ('featuring', models.ManyToManyField(blank=True, help_text='Enter staff members who feature in the episode (NOT including the host).', related_name='%(app_label)s_%(class)s_featuring_related', related_query_name='%(app_label)s_%(class)ss_featuring', to='fansite.Staff')),
                ('guests', models.ManyToManyField(blank=True, help_text='Enter any other guests (NOT official staff members).', to='fansite.Guest')),
                ('host', models.ForeignKey(blank=True, help_text='Enter staff member who hosts the episode.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_host_related', related_query_name='%(app_label)s_%(class)ss_host', to='fansite.staff')),
                ('main_segment_games', models.ManyToManyField(help_text='Enter any games part of the main segment of the Replay episode.', to='game.Game', verbose_name='Main Segment Games')),
                ('other_segments', models.ManyToManyField(blank=True, help_text='Enter other segments for the Replay episode.', to='fansite.Segment', verbose_name='Other Segments')),
                ('season', models.ForeignKey(help_text='Enter season of the Replay episode.', on_delete=django.db.models.deletion.CASCADE, to='fansite.replayseason', verbose_name='Replay Season')),
                ('thumbnails', models.ManyToManyField(blank=True, help_text='Enter thumbnail images for the episode.', to='fansite.Thumbnail')),
                ('youtube_video', models.OneToOneField(blank=True, help_text='Enter the YouTube video for the episode.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='fansite.youtubevideo', verbose_name='YouTube Video')),
            ],
            options={
                'verbose_name': 'Replay Episode',
                'ordering': ['-airdate'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HeadingInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.ForeignKey(help_text='Enter heading type.', on_delete=django.db.models.deletion.PROTECT, to='fansite.heading')),
            ],
            options={
                'verbose_name': 'Heading Instance',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(blank=True, help_text='Enter staff who authored the article.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='fansite.staff'),
        ),
    ]
