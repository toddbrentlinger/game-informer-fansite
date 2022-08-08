# Generated by Django 4.0.1 on 2022-08-07 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('games', '0003_remove_game_developer_remove_game_platform_and_more'),
        ('replay', '0001_initial'),
        ('shows', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuperReplay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter title of the super replay.', max_length=100)),
                ('number', models.SmallIntegerField(help_text='Enter Super Replay number (unofficial Super Replays use negative numbers).', unique=True)),
                ('headings', models.JSONField(blank=True, help_text='Enter JSON of different headings with key being the heading title and value being the content.', null=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('article', models.OneToOneField(blank=True, help_text='Enter article for the Super Replay.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='replay.article')),
                ('external_links', models.ManyToManyField(blank=True, help_text='Enter any external URL links (NOT including Game Informer article OR YouTube video).', to='shows.ExternalLink', verbose_name='External Links')),
            ],
            options={
                'verbose_name': 'Super Replay',
            },
        ),
        migrations.CreateModel(
            name='SuperReplayGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.OneToOneField(help_text='Enter game played in the Super Replay.', on_delete=django.db.models.deletion.CASCADE, to='games.game')),
                ('super_replay', models.ForeignKey(help_text='Enter Super Replay in which the game was played.', on_delete=django.db.models.deletion.CASCADE, to='superreplay.superreplay')),
            ],
        ),
        migrations.CreateModel(
            name='SuperReplayEpisode',
            fields=[
                ('episode_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shows.episode')),
                ('episode_number', models.PositiveSmallIntegerField(help_text='Enter episode number in the Super Replay.')),
                ('super_replay', models.ForeignKey(help_text='Enter Super Replay for this episode.', on_delete=django.db.models.deletion.CASCADE, to='superreplay.superreplay')),
            ],
            options={
                'verbose_name': 'Super Replay Episode',
                'ordering': ['airdate'],
            },
            bases=('shows.episode',),
        ),
    ]
