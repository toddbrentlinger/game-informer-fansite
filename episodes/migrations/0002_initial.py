# Generated by Django 4.0.1 on 2022-09-07 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('episodes', '0001_initial'),
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='featuring',
            field=models.ManyToManyField(blank=True, help_text='Enter people who feature in the episode (NOT including the host).', related_name='%(app_label)s_%(class)s_featuring_related', related_query_name='%(app_label)s_%(class)ss_featuring', to='people.Person'),
        ),
        migrations.AddField(
            model_name='episode',
            name='host',
            field=models.ForeignKey(blank=True, help_text='Enter person who hosts the episode.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_host_related', related_query_name='%(app_label)s_%(class)ss_host', to='people.person'),
        ),
        migrations.AddField(
            model_name='episode',
            name='youtube_video',
            field=models.OneToOneField(blank=True, help_text='Enter YouTube video of the episode.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='episodes.youtubevideo'),
        ),
    ]
