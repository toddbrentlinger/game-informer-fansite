# Generated by Django 4.0.1 on 2022-09-07 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('episodes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter name of the show.', max_length=100)),
                ('description', models.TextField(blank=True, help_text='Enter description of the show.')),
                ('slug', models.SlugField(help_text='Enter a url-safe, unique, lower-case version of the show.', max_length=100, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ShowEpisode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(help_text='Enter a url-safe, unique, lower-case version of the show episode.', max_length=100, unique=True)),
                ('episode', models.ForeignKey(help_text='Enter episode.', on_delete=django.db.models.deletion.CASCADE, to='episodes.episode')),
                ('show', models.ForeignKey(help_text='Enter show type of the episode.', on_delete=django.db.models.deletion.CASCADE, to='shows.show')),
            ],
        ),
    ]
