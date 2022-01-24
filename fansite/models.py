from asyncio.windows_events import NULL
import uuid # Used for unique model instances

from django.db import models
from django.urls import reverse

# Create your models here.

class Thumbnail(models.Model):
    """Model representing a thumbnail."""

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

    def __str__(self):
        return f'{self.url} ({self.get_quality_display()})'

# TODO: Use YouTube Data API
class YouTubeVideo(models.Model):
    """Model representing a YouTube video."""

    # Fields

    youtube_id = models.CharField(max_length=15, null=True, blank=True, verbose_name='video ID', help_text='Enter YouTube video ID') # YouTube ID has 11 characters
    views = models.PositiveBigIntegerField(null=True, blank=True, help_text='Enter number of views.')
    likes = models.PositiveIntegerField(null=True, blank=True, help_text='Enter number of likes.')
    dislikes = models.PositiveIntegerField(null=True, blank=True, help_text='Enter the number of dislikes.')
    thumbnails = models.ManyToManyField(Thumbnail, help_text='Enter thumbnail images for the video.')

    # Metadata
    # Methods

    def __str__(self):
        return self.youtube_id

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
    """Model representing a video game."""

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

    class Meta:
        ordering = ['title', 'release_date']

    # Methods

    def __str__(self):
        return f'{self.title} [{self.get_system_display()}]'

    def get_absolute_url(self):
        # game/metal-gear-solid-3
        pass

class Person(models.Model):
    """Abstract model representing a person."""

    # Fields

    first_name = models.CharField(max_length=100, verbose_name='first Name', help_text='Enter first name.')
    last_name = models.CharField(max_length=100, blank=True, verbose_name='last Name', help_text='Enter last name.')

    # Metadata

    class Meta:
        abstract = True
        ordering = ['last_name', 'first_name']

    # Methods

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Guest(Person):
    """Model representing a guest (not staff member)."""

    # Fields
    # Metadata
    # Methods

    def get_absolute_url(self):
        # guests/andrew-reiner
        pass

# TODO: Add validator to check end_date is greater than start_date
# TODO: Convert to StaffRole and intermediate class StaffRoleDuration (see Staff)
class StaffRole(models.Model):
    """Model representing a professional job role."""

    # Fields

    title = models.CharField(max_length=200, help_text='Enter title of professional role.')
    start_date = models.DateField(help_text='Enter date started the position.')
    end_date = models.DateField(help_text='Enter date started the position.')

    # Metadata

    class Meta:
        ordering = ['title']

    # Methods

    def __str__(self):
        return f'{self.title} [{self.start_date} - {self.end_date}]'

# TODO: Use 'Extra fields on many-to-many relationships' for roles, creating an 
# intermediate class RoleDuration to hold start_date, end_date, and anything else. 
class Staff(Person):
    """Model representing a staff member."""

    # Fields

    roles = models.ManyToManyField(StaffRole, help_text='Enter professional positions for staff member.')
    
    # Metadata
    # Methods
    
    def __str__(self):
        return f'{Person.__str__(self)} ({self.role})'

    def get_absolute_url(self):
        # staff/andrew-reiner
        # staff/tim-turi
        pass

class Article(models.Model):
    """Model representing an article."""

    # Fields

    title = models.CharField(max_length=100, help_text='Enter article title.')
    author = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, help_text='Enter staff who authored the article.')
    datetime = models.DateTimeField(help_text='Enter date and time article was published.')
    content = models.TextField(help_text='Enter main content of article.')

    # Metadata

    class Meta:
        ordering = ['-datetime']

    # Methods
    
    def __str__(self):
        return f'{self.title} by {self.author} on {self.datetime}'

# TODO: Create segment type as separate class so new segments can be added
# and convert this to SegmentInstance
class Segment(models.Model):
    """Model representing a segment of an episode."""

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
    games = models.ManyToManyField(Game, help_text='Enter games played during the segment.')

    # Metadata
    # Methods
    
    def __str__(self):
        pass

    def get_absolute_url(self):
        # replay/segments/rr
        # replay/segments/replay-roulette
        # replay/replay-roulette
        # ------------------------------------
        # replay/segments/youre-doing-it-wrong
        # replay/segments/doing-it-wrong
        pass

class ExternalLink(models.Model):
    """Model representing an external url link."""

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

    def __str__(self):
        return f'<a href={self.url}>{self.title}</a>'

    def getLinkSource(self):
        # Loop through EXTERNAL_LINK_SOURCES
            # If url contains first item of tuple
                # return second item of tuple
        # If reach this point, no match was found. Return default vaule
        pass

# TODO: Create heading type as separate model so new ones can be added dynamically.
# TODO: Different headings have different requirements. Description is just text, 
# quotes should be formatted differently, gallery includes images, etc.
class Heading(models.Model):
    """Model representing a specific heading with different content."""

    HEADING_TYPES = (
        ('description', 'Description'),
        ('gallery', 'Gallery'),
        ('quotes', 'Quotes'),
    )
    # Fields
    # Metadata
    # Methods
    pass

# TODO: Combine 'description' and 'other_headings' to 'headings'
class Episode(models.Model):
    """Abstract model representing a base episode."""

    # Fields

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, help_text='Enter episode title.')
    runtime = models.PositiveIntegerField(blank=True, help_text='Enter episode runtime as number of seconds.')
    thumbnails = models.ManyToManyField(Thumbnail, help_text='Enter thumbnail images for the episode.')
    airdate = models.DateField(help_text='Enter original date the episode first aired.')
    host = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, help_text='Enter staff member who hosts in the episode.')
    featuring = models.ManyToManyField(Staff, null=True, blank=True, help_text='Enter staff members who feature in the episode (NOT including the host).')
    description = models.TextField(max_length=10000, blank=True, help_text='Enter episode description')
    youtube_video = models.ForeignKey(YouTubeVideo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='youTube Video', help_text='Enter the YouTube video for the episode.')
    external_links = models.ManyToManyField(ExternalLink, null=True, blank=True, verbose_name='external Links', help_text='Enter any external URL links (NOT including Game Informer article OR YouTube video).')
    other_headings = models.ForeignKey(Heading, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='other Headings', help_text='Enter heading se')

    # Metadata

    class Meta:
        abstract = True
        ordering = ['-airdate']

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
    """Model representing an episode of Replay."""

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
        return Episode.__str__(self)

    def get_absolute_url(self):
        # replay/378 -> Replay Episode 378
        # replay/s2/45 -> Replay Season 2 Episode 45
        # replay/metal-gear-solid-3
        return reverse('replay', args=[str(self.id)])

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

class SuperReplay(models.Model):
    """Model representing a Super Replay."""

    # Fields
    # Metadata
    # Methods
    
    def __str__(self):
        pass

    def get_absolute_url(self):
        # super-replay/5 -> Super Replay 5
        # super-replay/Overblood -> Overblood Super Replay
        return reverse('super-replay', args=[str(self.id)])

class SuperReplayEpisode(Episode):
    """Model representing an episode of Super Replay."""

    # Fields

    super_replay = models.ForeignKey(SuperReplay, on_delete=models.CASCADE, help_text='Enter Super Replay for this episode.')

    # Metadata

    class Meta(Episode.Meta):
        ordering = ['airdate']

    # Methods
    
    def __str__(self):
        return Episode.__str__(self)

    def get_absolute_url(self):
        # super-replay/5/3 -> Super Replay 5 Episode 3
        # super-replay/Overblood/3 -> Overblood Super Replay Episode 3
        pass