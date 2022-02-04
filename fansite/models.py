import uuid # Used for unique model instances

from django.db import models
from django.urls import reverse

# Create your models here.

class Thumbnail(models.Model):
    """Model representing a thumbnail."""
    
    QualityType = models.TextChoices('QualityType', 'DEFAULT MEDIUM HIGH STANDARD MAXRES')

    # Fields

    quality = models.CharField(choices=QualityType.choices, max_length=20, help_text='Enter quality of thumbnail.')
    url = models.URLField(verbose_name='URL', help_text='Enter URL of thumbnail.')
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
        if (self.dislikes is NULL or self.likes is NULL):
            return 0

        # Check if both likes/dislikes are zero to avoid dividing by zero
        if (self.dislikes == 0 and self.likes == 0):
            return 0

        return round(round(self.likes/(self.likes + self.dislikes)) * 100, 1)

# TODO: Use VGDB (Video Game Database API)
# - *Could use API to fill a few basic fields to be stored on custom database and 
# use API whenever user accesses custom page for single game (ex. /game/metal-gear-solid-3)
# Which fields to store on custom database? (fields to sort/filter by)
#   -   Title, System, Release Date, Developer, Genres
# - Game model should hold system they played the game on since the IGDB shows all platforms per game ID,
# however IGDB displays separate release dates per system.
class Game(models.Model):
    """Model representing a video game."""

    # GAME_SYSTEMS = (
    #     ('PC', 'PC'),
    #     ('PS4', 'PlayStation 4'),
    #     ('X360', 'XBox 360'),
    # )

    # Fields

    igdb_id = models.PositiveIntegerField(null=True, blank=True, verbose_name='IGDB ID', help_text='Enter IGDB game ID to be used with API.')
    title = models.CharField(max_length=100, help_text='Enter game title.')
    system = models.CharField(max_length=30, help_text='Enter game system (ex. PC, PS4, XBox 360, etc.).')
    release_year = models.PositiveSmallIntegerField(verbose_name='Release Year', help_text='Enter date the game was released.')

    # Metadata

    class Meta:
        ordering = ['title', 'release_year']

    # Methods

    def __str__(self):
        return f'{self.title} [{self.system}]'

    # TODO: Use IGDB API to display information about the game as well as any stored
    # fields (ex. other episodes that include that game)
    def get_absolute_url(self):
        # game/metal-gear-solid-3
        pass

    def save(self, *args, **kwargs):
        super(Game, self).save(*args, **kwargs)

class Person(models.Model):
    """Abstract model representing a person."""

    # Fields

    first_name = models.CharField(max_length=100, verbose_name='First Name', help_text='Enter first name.')
    last_name = models.CharField(max_length=100, blank=True, verbose_name='Last Name', help_text='Enter last name.')

    # Metadata

    class Meta:
        abstract = True
        ordering = ['last_name', 'first_name']

    # Methods

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

# TODO: Use Person as normal class for guests since there's no extra functionality for Guest over generic Person class.
# However, do want separate detail page for guests and staff members.
class Guest(Person):
    """Model representing a guest (not staff member)."""

    # Fields
    # Metadata
    # Methods

    def get_absolute_url(self):
        # guests/hilary-wilton
        pass

# TODO: Use 'Extra fields on many-to-many relationships' for roles, creating an 
# intermediate class RoleDuration to hold start_date, end_date, and anything else. 
class Staff(Person):
    """Model representing a staff member."""

    # Fields
    # Metadata

    class Meta:
        verbose_name = 'Staff Member'
        verbose_name_plural = 'Staff'

    # Methods

    def get_absolute_url(self):
        # staff/andrew-reiner
        # staff/tim-turi
        return reverse('staff', args=[str(self.id)])

class StaffPosition(models.Model):
    """Model representing a specific position at the company."""

    # Fields

    title = models.CharField(max_length=200, help_text='Enter title of position.')

    # Metadata

    class Meta:
        ordering = ['title']
        verbose_name = 'Staff Position'

    # Methods

    def __str__(self):
        return self.title

# TODO: Add validator to check end_date is greater than start_date
# TODO: Convert to StaffRole and intermediate class StaffRoleDuration (see Staff)
class StaffPositionInstance(models.Model):
    """Model representing a single instance of a position at the company."""

    # Fields

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, help_text='Enter staff member for this position instance.')
    position = models.ForeignKey(StaffPosition, on_delete=models.PROTECT, help_text='Enter position of the staff member.')
    start_year = models.PositiveSmallIntegerField(verbose_name='Start Year', help_text='Enter date started the position.')
    end_year = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='End Year', help_text='Enter date started the position.')

    # Metadata

    class Meta:
        ordering = ['-start_year']
        verbose_name = 'Staff Position Instance'

    # Methods

    def __str__(self):
        return f'{self.position} [{self.start_date} - {self.end_date}]'

class Article(models.Model):
    """Model representing an article."""

    # Fields

    title = models.CharField(max_length=100, help_text='Enter article title.')
    author = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, help_text='Enter staff who authored the article.')
    datetime = models.DateTimeField(help_text='Enter date and time article was published.')
    content = models.TextField(help_text='Enter main content of article.')
    url = models.URLField(null=True, verbose_name='URL', help_text='Enter URL of article.')

    # Metadata

    class Meta:
        ordering = ['-datetime']

    # Methods
    
    def __str__(self):
        return f'{self.title} by {self.author} on {self.datetime.strftime("%b %d, %Y at %I:%M %p")}'

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
    # )

    # Fields

    title = models.CharField(max_length=100, help_text='Enter title of segment.')
    abbreviation = models.CharField(max_length=10, blank=True, help_text='Enter shortened abbreviation of segment title.')
    description = models.CharField(max_length=1000, blank=True, help_text='Enter description of segment.')

    # Metadata

    class Meta:
        ordering = ['title']
        verbose_name = 'Segment Type'

    # Methods

    def __str__(self):
        return self.title

class Segment(models.Model):
    """Model representing a single instance of a segment in an episode."""

    # Fields

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text='Unique ID for this particular segment instance.')
    segment_type = models.ForeignKey(SegmentType, on_delete=models.PROTECT, help_text='Enter type of segment.')
    games = models.ManyToManyField(Game, blank=True, help_text='Enter games played during the segment.')
    content = models.TextField(blank=True, help_text='Enter content description of this segment instance.')
    
    # Metadata

    class Meta:
        pass

    # Methods
    
    def __str__(self):
        return f'{self.segment_type} - {self.games}'

    def get_absolute_url(self):
        # replay/segments/rr
        # replay/segments/replay-roulette
        # replay/replay-roulette
        # ------------------------------------
        # replay/segments/youre-doing-it-wrong
        # replay/segments/doing-it-wrong
        pass

    def display_games(self):
        return ', '.join(game.__str__() for game in self.games.all()[:3])
    
    display_games.short_description = 'Games'

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
            # If url contains first item of tuple
                # return second item of tuple
        # If reach this point, no match was found. Return default vaule
        pass

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

# TODO: Combine 'description' and 'other_headings' to 'headings'
# TODO: Combine next two into single headingInstances = ForeignKey but ForeignKey should be inside 'one' of 'one-to-many' relationship.
# This should be inside HeadingInstance class as an 'episode' property. More is required since it makes more sense to adding new HeadingInstances
# when creating an Episode instead of adding an Episode when creating a HeadingInstance.
# *** Use 'django polymorphic' on base abstract class 'Heading' with child classes TextHeading, ImageGalleryHeading, QuoteHeading, ListHeading.
# TODO: Combine 'host', 'featuring', and 'guests' into single 'featuring'. 
# Could create separate Featuring class to hold 'host', 'staff', and 'guests'
# OR use another 'django polymorphic' on base abstract class 'Person'
class Episode(models.Model):
    """Abstract model representing a base episode."""

    # Fields

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, help_text='Enter episode title.')
    # nn:nn:nn (ex. 01:35:23 for 1hr 35min 23sec)
    runtime = models.CharField(max_length=10, blank=True, help_text='Enter episode runtime in format hh:mm:ss.')
    thumbnails = models.ManyToManyField(Thumbnail, blank=True, help_text='Enter thumbnail images for the episode.')
    airdate = models.DateField(help_text='Enter original date the episode first aired.')
    host = models.ForeignKey(Staff, related_name='%(app_label)s_%(class)s_host_related', related_query_name='%(app_label)s_%(class)ss_host', on_delete=models.SET_NULL, null=True, blank=True, help_text='Enter staff member who hosts the episode.')
    featuring = models.ManyToManyField(Staff, related_name='%(app_label)s_%(class)s_featuring_related', related_query_name='%(app_label)s_%(class)ss_featuring', blank=True, help_text='Enter staff members who feature in the episode (NOT including the host).')
    guests = models.ManyToManyField(Guest, blank=True, help_text='Enter any other guests (NOT official staff members).')
    youtube_video = models.ForeignKey(YouTubeVideo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='youTube Video', help_text='Enter the YouTube video for the episode.')
    external_links = models.ManyToManyField(ExternalLink, blank=True, verbose_name='External Links', help_text='Enter any external URL links (NOT including Game Informer article OR YouTube video).')
    #description = models.TextField(max_length=10000, blank=True, help_text='Enter episode description')
    #other_headings = models.ForeignKey(HeadingInstance, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Other Headings', help_text='Enter heading se')
    headings = models.JSONField(null=True, blank=True, help_text='Enter JSON of different headings with key being the heading title and value being the content.')

    # Metadata

    class Meta:
        abstract = True
        ordering = ['-airdate']

    # Methods

    def __str__(self):
        return self.title

    def display_featuring(self):
        return ', '.join( person.__str__() for person in (self.featuring.all()[:3] + self.guests.all()[:3]) )

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

# TODO: Replace 'middle_segment' and 'second_segment' with 'segments' ManyToManyField
class ReplayEpisode(Episode):
    """Model representing an episode of Replay."""

    # Fields

    number = models.SmallIntegerField(unique=True, help_text='Enter Replay episode number (unofficial episodes use negative numbers).')
    main_segment_games = models.ManyToManyField(Game, verbose_name='Main Segment Games', help_text='Enter any games part of the main segment of the Replay episode.')
    middle_segment = models.ForeignKey(Segment, related_name='%(app_label)s_%(class)s_middle_segment_related', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Middle Segment', help_text='Enter middle segment for the Replay episode.')
    second_segment = models.ForeignKey(Segment, related_name='%(app_label)s_%(class)s_second_segment_related', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Second Segment', help_text='Enter second segment for the Replay episode.')
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

    class Meta:
        verbose_name = 'Super Replay'

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
        verbose_name = 'Super Replay Episode'

    # Methods
    
    def __str__(self):
        return Episode.__str__(self)

    def get_absolute_url(self):
        # super-replay/5/3 -> Super Replay 5 Episode 3
        # super-replay/Overblood/3 -> Overblood Super Replay Episode 3
        pass