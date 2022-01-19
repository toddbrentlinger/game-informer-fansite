from asyncio.windows_events import NULL
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
    GAME_SYSTEMS = (
        ('PC', 'PC'),
        ('PS4', 'PlayStation 4'),
        ('X360', 'XBox 360'),
    )

    # Fields

    title = models.CharField(max_length=100, help_text='Enter game title.')
    system = models.CharField(max_length=10, choices=GAME_SYSTEMS, help_text='Enter game system (ex. PC, PS4, XBox 360, etc.).')
    release_date = models.DateField(help_text='Enter date the game was released.')

    # Metadata
    # Methods

class Person(models.Model):
    # Fields

    first_name = models.CharField(max_length=100, help_text='Enter first name.')
    last_name = models.CharField(max_length=100, help_text='Enter last name.')

    # Metadata

    class Meta:
        abstract = True

    # Methods

class Guest(Person):
    # Fields
    # Metadata
    # Methods
    pass

class Staff(Person):
    # Fields
    # Metadata
    # Methods
    pass

class Article(models.Model):
    # Fields

    title = models.CharField(max_length=100, help_text='Enter article title.')
    author = NULL
    datetime = models.DateTimeField(help_text='Enter date and time article was published.')
    content = models.TextField(help_text='Enter main content of article.')

    # Metadata
    # Methods

class Segment(models.Model):
    # Fields
    # Metadata
    # Methods
    pass

class ExternalLink(models.Model):
    # Fields

    url = models.CharField(max_length=500, help_text='Enter URL of external link.')
    title = models.CharField(max_length=100, help_text='Enter display title of external link.')

    # Metadata
    # Methods

class OtherHeading(models.Model):
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
    featuring = models.ManyToManyField(Staff, blank=True, help_text='Enter staff members who feature in the episode (NOT including the host).')
    description = models.TextField(max_length=10000, blank=True, help_text='Enter episode description')
    youtube_video = models.ForeignKey(YouTubeVideo, blank=True, help_text='Enter the YouTube video for the episode.')
    external_links = models.ManyToManyField(ExternalLink, help_text='Enter any external URL links (NOT including Game Informer article OR YouTube video).')
    other_headings = models.ForeignKey(OtherHeading, help_text='Enter heading se')

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

    def getSeason(self):
        replaySeasonStartEpisodes = [1, 107, 268, 385, 443, 499] # [S1, S2, S3, S4, S5, S6]
        # Return tuple (season, seasonEpisode)

class SuperReplayEpisode(Episode):
    # Fields
    # Metadata

    class Meta(Episode.Meta):
        pass

    # Methods