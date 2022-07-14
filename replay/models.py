import uuid # used for unique model instances
import re

from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from games.models import Game
from people.models import Person

# Create your models here.

# Abstract Models

# TODO: Convert external_links to JSON field instead. Saving unique instances of links does not seem necessary.
# X TODO: Combine 'description' and 'other_headings' to 'headings'
# TODO: Combine next two into single headingInstances = ForeignKey but ForeignKey should be inside 'one' of 'one-to-many' relationship.
# This should be inside HeadingInstance class as an 'episode' property. More is required since it makes more sense to adding new HeadingInstances
# when creating an Episode instead of adding an Episode when creating a HeadingInstance.
# *** Use 'django polymorphic' on base abstract class 'Heading' with child classes TextHeading, ImageGalleryHeading, QuoteHeading, ListHeading.
# TODO: Combine 'host', 'featuring', and 'guests' into single 'featuring'. 
# Could create separate Featuring class to hold 'host', 'staff', and 'guests'
# OR use another 'django polymorphic' on base abstract class 'Person'
# 2/21/22 - Could use HStoreField importing from django.contrib.postgres.fields which stores key/value pairs for 'headings' field.
# 3/6/22 - Headings Issue: Could create abstract model 'Heading', then create different type of headings (Text, Quotes, Gallery, etc)
# with ForeignKey field 'episode'. Episode could have multiple TextHeadings but TextHeading has only one episode.
# ISSUE: How to reference abstract field Episode inside TextHeading, QuotesHeading, etc.?
class Episode(models.Model):
    """Abstract model representing a base episode."""

    # Fields

    # TODO: Should UUID be primary key or is built-in primary key sufficient?
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, help_text='Enter episode title.')
    # TODO: Runtime should be in youtube_video after using YouTube API. 
    # One few videos do not have YouTube id but does have runtime (videos never on YouTube).
    # nn:nn:nn (ex. 01:35:23 for 1hr 35min 23sec)
    runtime = models.CharField(max_length=10, blank=True, help_text='Enter episode runtime in format hh:mm:ss.')
    # NOTE: If no YouTube video, display default image in HTML. Not necessary to keep separate 'thumbnails' property
    # unless episode has NO YouTube video but does have thumbnail from Fandom Wiki.
    #thumbnails = models.ManyToManyField(Thumbnail, blank=True, help_text='Enter thumbnail images for the episode.')
    airdate = models.DateField(help_text='Enter original date the episode first aired.')
    host = models.ForeignKey(Person, related_name='%(app_label)s_%(class)s_host_related', related_query_name='%(app_label)s_%(class)ss_host', on_delete=models.SET_NULL, null=True, blank=True, help_text='Enter person who hosts the episode.')
    featuring = models.ManyToManyField(Person, related_name='%(app_label)s_%(class)s_featuring_related', related_query_name='%(app_label)s_%(class)ss_featuring', blank=True, help_text='Enter people who feature in the episode (NOT including the host).')
    youtube_video = models.OneToOneField('YouTubeVideo', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='YouTube Video', help_text='Enter the YouTube video for the episode.')
    external_links = models.ManyToManyField('ExternalLink', blank=True, verbose_name='External Links', help_text='Enter any external URL links (NOT including Game Informer article OR YouTube video).')
    #description = models.TextField(max_length=10000, blank=True, help_text='Enter episode description')
    #other_headings = models.ForeignKey(HeadingInstance, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Other Headings', help_text='Enter heading se')
    headings = models.JSONField(null=True, blank=True, help_text='Enter JSON of different headings with key being the heading title and value being the content.')
    slug = models.SlugField(max_length=100, unique=True, null=False)

    # Metadata

    class Meta:
        abstract = True
        ordering = ['-airdate']

    # Methods

    def __str__(self):
        return self.title

    def display_featuring(self):
        return ', '.join( person.__str__() for person in self.featuring.all()[:3] )

    display_featuring.short_description = 'Featuring'

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

# Models

'''
TODO:
X Use base Person class for Staff and Guests instead of deriving from abstract Person class.
Inside Staff class, replace char field 'name' with OneToOneField 'person'.
Can remove Guests class entirely. Simply filter Person class that are NOT Staff.
- Remove ReplayEpisode.thumbnails field. Use Replay.youtube_video.thumbnails instead. 
If ReplayEpisode is null, use same base thumbnails in view. 
No need to save base thumbnails in database.
'''

class Article(models.Model):
    """Model representing an article."""

    # Fields

    title = models.CharField(max_length=100, help_text='Enter article title.')
    author = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, help_text='Enter person who authored the article.')
    datetime = models.DateTimeField(help_text='Enter date and time article was published.')
    content = models.TextField(help_text='Enter main content of article.')
    url = models.URLField(null=True, verbose_name='URL', help_text='Enter URL of article.')

    # Metadata

    class Meta:
        ordering = ['-datetime']

    # Methods
    
    def __str__(self):
        return f'{self.title} by {self.author} on {self.datetime.strftime("%b %d, %Y at %I:%M %p")}'

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

    url = models.URLField(verbose_name='URL', help_text='Enter URL of external link.')
    title = models.CharField(max_length=100, help_text='Enter display title of external link.')

    # Metadata

    class Meta:
        verbose_name = 'External Link'

    # Methods

    def __str__(self):
        return f'{self.title} - {self.url}'

    def create_anchor_link(self):
        return f'<a href={self.url}>{self.title}</a>'

    def getLinkSource(self):
        # Loop through EXTERNAL_LINK_SOURCES
        for match_str, source in self.EXTERNAL_LINK_SOURCES:
            # If url contains first item of tuple
            if match_str in self.url:
                # return second item of tuple
                return source
        # If reach this point, no match was found. Return default value
        return None

class Heading(models.Model):
    """Model representing a type of heading of an episode."""

    # HEADING_TYPES = (
    #     ('description', 'Description'),
    #     ('gallery', 'Gallery'),
    #     ('quotes', 'Quotes'),
    # )

    # Fields

    title = models.CharField(max_length=100, help_text='Enter heading title.')

    # Metadata
    # Methods

    def __str__(self):
        return self.title

# TODO: Different headings have different requirements. Description is just text, 
# quotes should be formatted differently, gallery includes images, etc.
class HeadingInstance(models.Model):
    """Model representing a specific heading with different content."""

    # Fields

    heading = models.ForeignKey(Heading, on_delete=models.PROTECT, help_text='Enter heading type.')
    #episode = models.ForeignKey('Episode', on_delete=models.CASCADE, help_text='Enter episode for which this heading instance belongs.')

    # Metadata

    class Meta:
        verbose_name = 'Heading Instance'

    # Methods
    
    def __str__(self):
        pass

# TODO: Replace 'middle_segment' and 'second_segment' with 'segments' ManyToManyField.
# Should add main segment inside segments instead of having separate field just for main segment games?
class ReplayEpisode(Episode):
    """Model representing an episode of Replay."""

    # Fields

    season = models.ForeignKey('ReplaySeason', on_delete=models.CASCADE, verbose_name='Replay Season', help_text='Enter season of the Replay episode.')
    number = models.SmallIntegerField(unique=True, help_text='Enter Replay episode number (unofficial episodes use negative numbers).')
    main_segment_games = models.ManyToManyField(Game, verbose_name='Main Segment Games', help_text='Enter any games part of the main segment of the Replay episode.')
    other_segments = models.ManyToManyField('Segment', blank=True, verbose_name='Other Segments', help_text='Enter other segments for the Replay episode.')
    # middle_segment = models.ForeignKey(Segment, related_name='%(app_label)s_%(class)s_middle_segment_related', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Middle Segment', help_text='Enter middle segment for the Replay episode.')
    # second_segment = models.ForeignKey(Segment, related_name='%(app_label)s_%(class)s_second_segment_related', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Second Segment', help_text='Enter second segment for the Replay episode.')
    article = models.OneToOneField(Article, on_delete=models.SET_NULL, null=True, blank=True, help_text='Enter article for the Replay episode.')

    # Metadata

    class Meta(Episode.Meta):
        verbose_name = 'Replay Episode'

    # Methods
    
    def __str__(self):
        return Episode.__str__(self)

    def get_absolute_url(self):
        # replay/378 -> Replay Episode 378
        # replay/s2/45 -> Replay Season 2 Episode 45
        # replay/metal-gear-solid-3
        return reverse('replay-detail-slug', kwargs={'stub': self.slug})
        #return reverse('replay-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(re.sub(r'Replay:\s?', '', self.title, 1, re.IGNORECASE))
        return super(ReplayEpisode, self).save(*args, **kwargs)

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
    get_season.short_description = 'Season'

class ReplaySeason(models.Model):
    # Fields

    # n=0 for unofficial episodes and n>0 for regular seasons 
    number = models.SmallIntegerField(primary_key=True, help_text='Enter unique number of Replay season.')
    description = models.TextField(blank=True, help_text='Enter description for the Replay season.')

    # Metadata

    class Meta:
        ordering = ['-number']
        verbose_name = 'Replay Season'

    # Methods
    
    def __str__(self):
        return str(self.number)

    def get_absolute_url(self):
        # replay/s2
        # replay/s0 - unofficial
        return reverse('replay-season', args=[str(self.number)])

class Segment(models.Model):
    """Model representing a single instance of a segment in an episode."""

    # Fields

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text='Unique ID for this particular segment instance.')
    type = models.ForeignKey('SegmentType', on_delete=models.PROTECT, help_text='Enter type of segment.')
    games = models.ManyToManyField(Game, blank=True, help_text='Enter games played during the segment.')
    description = models.TextField(blank=True, help_text='Enter description of this segment instance.')
    
    # Metadata

    class Meta:
        pass

    # Methods
    
    def __str__(self):
        if self.games.exists():
            return f'{self.type} - {self.display_games()}'
        else:
            return str(self.type)

    def display_games(self):
        return ', '.join(game.__str__() for game in self.games.all()[:3])
    
    display_games.short_description = 'Games'

class SegmentType(models.Model):
    """Model representing a segment of an episode."""

    # SEGMENT_TYPES = (
    #     ('RR', 'Replay Roulette'),
    #     ('SRS', 'Super Replay Showdown'),
    #     ('YDIW', 'You\'re Doing It Wrong'),
    #     ('ST', 'Stress Test'),
    #     ('RP', 'RePorted'),
    #     ('DP', 'Developer Pick'),
    #     ('2037', 'Replay 2037'),
    #     ('HF', 'Horror Fest'),
    #     ('RRL', 'Replay Real Life'),
    #     ('AD', 'Advertisement'),
    # )

    # Fields

    title = models.CharField(max_length=100, help_text='Enter title of segment.')
    abbreviation = models.CharField(max_length=10, blank=True, help_text='Enter shortened abbreviation of segment title.')
    description = models.TextField(blank=True, help_text='Enter description of segment.')
    slug = models.SlugField(max_length=100, unique=True, null=False)

    # Metadata

    class Meta:
        ordering = ['title']
        verbose_name = 'Segment Type'

    # Methods

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # replay/segments/rr
        # replay/segments/replay-roulette
        # replay/replay-roulette
        # ------------------------------------
        # replay/segments/youre-doing-it-wrong
        # replay/segments/doing-it-wrong
        return reverse('segment-type-detail-slug', kwargs={'stub': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(SegmentType, self).save(*args, **kwargs)

class Thumbnail(models.Model):
    """Model representing a thumbnail."""
    
    QualityType = models.TextChoices('QualityType', 'DEFAULT MEDIUM HIGH STANDARD MAXRES')

    # Fields

    quality = models.CharField(choices=QualityType.choices, default=QualityType.DEFAULT, max_length=20, help_text='Enter quality of thumbnail.')
    url = models.URLField(unique=True, verbose_name='URL', help_text='Enter URL of thumbnail.')
    width = models.PositiveSmallIntegerField(help_text='Enter width of thumbnail')
    height = models.PositiveSmallIntegerField(help_text='Enter height of thumbnail')
    
    # Metadata
    # Methods

    def __str__(self):
        return f'{self.url} ({self.get_quality_display()})'

    def create_srcset_entry(self):
        return f'{self.url} {self.width}w'

# TODO: Use YouTube Data API
class YouTubeVideo(models.Model):
    """Model representing a YouTube video."""

    # Fields

    youtube_id = models.CharField(max_length=15, blank=True, verbose_name='Video ID', help_text='Enter YouTube video ID') # YouTube ID has 11 characters
    title = models.CharField(max_length=100, help_text='Enter title of the video.')
    views = models.PositiveBigIntegerField(null=True, blank=True, help_text='Enter number of views.')
    likes = models.PositiveIntegerField(null=True, blank=True, help_text='Enter number of likes.')
    dislikes = models.PositiveIntegerField(null=True, blank=True, help_text='Enter the number of dislikes.')
    thumbnails = models.ManyToManyField(Thumbnail, help_text='Enter thumbnail images for the video.')

    # Metadata

    class Meta:
        verbose_name = 'YouTube Video'

    # Methods

    def __str__(self):
        return f'{self.youtube_id} - {self.title}'

    @property
    def like_ratio(self):
        # 
        if (self.dislikes is None or self.likes is None):
            return 0

        # Check if both likes/dislikes are zero to avoid dividing by zero
        if (self.dislikes == 0 and self.likes == 0):
            return 0

        return round(round(self.likes/(self.likes + self.dislikes)) * 100, 1)