from asyncio.windows_events import NULL
import uuid # Used for unique model instances

from django.db import models

# Create your models here.

class Thumbnail(models.Model):
    QualityType = models.TextChoices(
        'default', 'medium', 'high', 'standard', 'maxres',
    )

    # Fields

    quality = models.CharField(choices=QualityType.choices, max_length=20, help_text='Enter quality of thumbnail.')
    url = models.URLField(help_text='Enter URL of thumbnail.')
    width = models.PositiveSmallIntegerField(help_text='Enter width of thumbnail')
    height = models.PositiveSmallIntegerField(help_text='Enter height of thumbnail')

    # Metadata
    # Methods

class YouTubeVideo(models.Model):
    # Fields

    youtube_id = models.CharField(max_length=15, null=True, blank=True, verbose_name='video ID', help_text='Enter YouTube video ID') # YouTube ID has 11 characters
    views = models.PositiveBigIntegerField(null=True, blank=True, help_text='Enter number of views.')
    likes = models.PositiveIntegerField(null=True, blank=True, help_text='Enter number of likes.')
    dislikes = models.PositiveIntegerField(null=True, blank=True, help_text='Enter the number of dislikes.')
    thumbnails = models.ManyToManyField(Thumbnail, help_text='Enter thumbnail images for the video.')

    # Metadata
    # Methods

    @property
    def like_ratio(self):
        # 
        if (self.dislikes is NULL or self.likes is NULL):
            return 0

        # Check if both likes/dislikes are zero to avoid dividing by zero
        if (self.dislikes == 0 and self.likes == 0):
            return 0

        return round(round(self.likes/(self.likes + self.dislikes)) * 100, 1)

# TODO: Use VGDB (Video Game Database API)
class Game(models.Model):
    GAME_SYSTEMS = (
        ('PC', 'PC'),
        ('PS4', 'PlayStation 4'),
        ('X360', 'XBox 360'),
    )

    # Fields

    title = models.CharField(max_length=100, help_text='Enter game title.')
    system = models.CharField(max_length=10, choices=GAME_SYSTEMS, help_text='Enter game system (ex. PC, PS4, XBox 360, etc.).')
    release_date = models.DateField(verbose_name='release Date', help_text='Enter date the game was released.')

    # Metadata
    # Methods

class Person(models.Model):
    # Fields

    first_name = models.CharField(max_length=100, verbose_name='first Name', help_text='Enter first name.')
    last_name = models.CharField(max_length=100, verbose_name='last Name', help_text='Enter last name.')

    # Metadata

    class Meta:
        abstract = True

    # Methods

class Guest(Person):
    # Fields
    # Metadata
    # Methods
    
    def __str__(self):
        pass

    def get_absolute_url(self):
        pass

class Staff(Person):
    # Fields

    role = models.CharField(max_length=200, help_text='Enter professional role of staff member.')

    # Metadata
    # Methods
    
    def __str__(self):
        pass

    def get_absolute_url(self):
        pass

class Article(models.Model):
    # Fields

    title = models.CharField(max_length=100, help_text='Enter article title.')
    author = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, help_text='Enter staff who authored the article.')
    datetime = models.DateTimeField(help_text='Enter date and time article was published.')
    content = models.TextField(help_text='Enter main content of article.')

    # Metadata
    # Methods
    
    def __str__(self):
        pass

class Segment(models.Model):
    SEGMENT_TYPES = (
        ('RR', 'Replay Roulette'),
        ('SRS', 'Super Replay Showdown'),
        ('YDIW', 'You\'re Doing It Wrong'),
        ('ST', 'Stress Test'),
        ('RP', 'RePorted'),
        ('DP', 'Developer Pick'),
        ('2037', 'Replay 2037'),
        ('HF', 'Horror Fest'),
        ('RRL', 'Replay Real Life'),
    )

    # Fields

    type = models.CharField(max_length=10, choices=SEGMENT_TYPES, help_text='Enter type of segment.')

    # Metadata
    # Methods
    
    def __str__(self):
        pass

    def get_absolute_url(self):
        pass

class ExternalLink(models.Model):
    # TODO: Used to display source of url: <title> on <source>
    EXTERNAL_LINK_SOURCES = (
        ('gameinformer', 'Game Informer'),
        ('youtube', 'YouTube'),
        ('fandom', 'Fandom'),
        ('wikipedia', 'Wikipedia'),
        ('gamespot', 'GameSpot'),
        ('steampowered', 'Steam'),
    )

    # Fields

    url = models.URLField(help_text='Enter URL of external link.')
    title = models.CharField(max_length=100, help_text='Enter display title of external link.')

    # Metadata
    # Methods

    def getLinkSource(self):
        # Loop through EXTERNAL_LINK_SOURCES
            # If url contains first item of tuple
                # return second item of tuple
        # If reach this point, no match was found. Return default vaule
        pass

class OtherHeading(models.Model):
    # Fields
    # Metadata
    # Methods
    pass

class Episode(models.Model):
    # Fields

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, help_text='Enter episode title.')
    runtime = models.PositiveIntegerField(blank=True, help_text='Enter episode runtime as number of seconds.')
    thumbnails = models.ManyToManyField(Thumbnail, help_text='Enter thumbnail images for the episode.')
    airdate = models.DateField(help_text='Enter original date the episode first aired.')
    host = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, help_text='Enter staff member who hosts in the episode.')
    featuring = models.ManyToManyField(Staff, null=True, blank=True, help_text='Enter staff members who feature in the episode (NOT including the host).')
    description = models.TextField(max_length=10000, blank=True, help_text='Enter episode description')
    youtube_video = models.ForeignKey(YouTubeVideo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='youTube Video', help_text='Enter the YouTube video for the episode.')
    external_links = models.ManyToManyField(ExternalLink, null=True, blank=True, verbose_name='external Links', help_text='Enter any external URL links (NOT including Game Informer article OR YouTube video).')
    other_headings = models.ForeignKey(OtherHeading, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='other Headings', help_text='Enter heading se')

    # Metadata

    class Meta:
        abstract = True

    # Methods

    def __str__(self):
        return self.title

    def convertRuntimeToSeconds(self, runtimeStr):
        '''Takes duration parameter in form 00:00:00 and returns total number of seconds'''
        digits = [int(digit) for digit in runtimeStr.split(':')]
        len_digits = len(digits)
        
        # Seconds in seconds digit
        seconds = digits[len_digits - 1]
        # Seconds in minutes digit
        minutes = digits[len_digits - 2] * 60 if len_digits > 1 else 0
        # Seconds in hours digit
        hours = digits[len_digits - 3] * 3600 if len_digits > 2 else 0
        
        return seconds + minutes + hours

class ReplayEpisode(Episode):
    # Fields

    number = models.SmallIntegerField(unique=True, help_text='Enter Replay episode number (unofficial episodes use negative numbers).')
    main_segment_games = models.ManyToManyField(Game, verbose_name='main Segment Games', help_text='Enter any games part of the main segment of the Replay episode.')
    middle_segment = models.ForeignKey(Segment, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='middle Segment', help_text='Enter middle segment for the Replay episode.')
    second_segment = models.ForeignKey(Segment, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='second Segment', help_text='Enter second segment for the Replay episode.')
    article = models.OneToOneField(Article, null=True, blank=True, help_text='Enter article for the Replay episode.')

    # Metadata

    class Meta(Episode.Meta):
        pass

    # Methods
    
    def __str__(self):
        pass

    def get_absolute_url(self):
        pass

    def get_season(self):
        # Episode numbers less than 1 are special unofficial episodes
        replaySeasonStartEpisodes = [1, 107, 268, 385, 443, 499] # [S1, S2, S3, S4, S5, S6]

        # Season
        
        for index in range(len(replaySeasonStartEpisodes)):
            if (self.number < replaySeasonStartEpisodes[index]):
                season = index
                break
            # If reached end of loop, assign last season
            if index == (len(replaySeasonStartEpisodes) - 1):
                season = len(replaySeasonStartEpisodes)

        # Season Episode

        seasonEpisode = self.number - replaySeasonStartEpisodes[season - 1] + 1 if season > 1 else self.number

        # Return tuple (season, seasonEpisode)
        return (season, seasonEpisode)

class SuperReplayEpisode(Episode):
    # Fields
    # Metadata

    class Meta(Episode.Meta):
        pass

    # Methods
    
    def __str__(self):
        pass

    def get_absolute_url(self):
        pass