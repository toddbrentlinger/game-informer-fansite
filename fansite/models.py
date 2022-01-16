from django.db import models

# Create your models here.

class YouTubeVideo(models.Model):
    # Fields

    youtube_id = models.CharField(max_length=15) # YouTube ID has 11 characters
    views = models.PositiveIntegerField(help_text='Enter number of views.')
    likes = models.PositiveIntegerField(help_text='Enter number of likes.')
    dislikes = models.PositiveIntegerField(help_text='Enter the number of dislikes.')

    # Metadata
    # Methods

class Thumbnail(models.Model):
    # Fields
    # Metadata
    # Methods
    pass

class Game(models.Model):
    # Fields
    # Metadata
    # Methods
    pass

class Staff(models.Model):
    # Fields
    # Metadata
    # Methods
    pass

class Article(models.Model):
    # Fields
    # Metadata
    # Methods
    pass

class Segment(models.Model):
    # Fields
    # Metadata
    # Methods
    pass

class Episode(models.Model):
    # Fields

    title = models.CharField(max_length=100, help_text='Enter episode title.')
    runtime = models.PositiveIntegerField(help_text='Enter episode runtime as number of seconds.')
    thumbnails = models.ManyToManyField(Thumbnail, help_text='Enter thumbnail images for the episode.')
    airdate = models.DateField(help_text='Enter original date the episode first aired.')
    host = models.ForeignKey(Staff, help_text='Enter staff member who hosts in the episode.')
    featuring = models.ManyToManyField(Staff, help_text='Enter staff members who features in the episode.')
    description = models.TextField(max_length=10000, help_text='Enter episode description')
    youtube_video = models.ForeignKey(YouTubeVideo, help_text='Enter the YouTube video for the episode.')

    # Metadata

    class Meta:
        abstract = True

    # Methods

    def __str__(self):
        return self.title

class ReplayEpisode(Episode):
    # Fields

    number = models.PositiveIntegerField(help_text='Enter Replay episode number.')
    main_segment_games = models.ManyToManyField(Game, help_text='Enter any games part of the main segment of the Replay episode.')
    middle_segment = models.ForeignKey(Segment, help_text='Enter middle segment for the Replay episode.')
    second_segment = models.ForeignKey(Segment, help_text='Enter second segment for the Replay episode.')
    article = models.OneToOneField(Article, help_text='Enter article for the Replay episode.')

    # Metadata

    class Meta(Episode.Meta):
        pass

    # Methods

class SuperReplayEpisode(Episode):
    # Fields
    # Metadata

    class Meta(Episode.Meta):
        pass

    # Methods