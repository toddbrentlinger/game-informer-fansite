import re

from django.db import models
from django.urls import reverse

from people.models import Person

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
# 8/19/22 - Move main_segment_games field from ReplayEpisode to Episode?
# 9/13/22 - Make youtube_video field unique. Can field be unique AND blank? Yes, Null !== Null
class Episode(models.Model):
    # Fields

    #shows = models.ManyToManyField('shows.Show', blank=True, help_text='Enter shows that include the episode.')
    title = models.CharField(max_length=100, help_text='Enter title of the episode.')
    host = models.ForeignKey(Person, related_name='%(app_label)s_%(class)s_host_related', related_query_name='%(app_label)s_%(class)ss_host', on_delete=models.SET_NULL, null=True, blank=True, help_text='Enter person who hosts the episode.')
    featuring = models.ManyToManyField(Person, related_name='%(app_label)s_%(class)s_featuring_related', related_query_name='%(app_label)s_%(class)ss_featuring', blank=True, help_text='Enter people who feature in the episode (NOT including the host).')
    youtube_video = models.OneToOneField('YouTubeVideo', unique=True, blank=True, null=True, on_delete=models.SET_NULL, help_text='Enter YouTube video of the episode.')
    external_links = models.ManyToManyField('ExternalLink', blank=True, verbose_name='External Links', help_text='Enter any external URL links (NOT including YouTube video).')
    headings = models.JSONField(null=True, blank=True, help_text='Enter JSON of different headings with key being the heading title and value being the content.')
    # TODO: Move slug into ReplayEpisode and SuperReplayEpisode in case of YouTube title duplicates
    slug = models.SlugField(max_length=100, unique=True, null=False, help_text='Enter a url-safe, unique, lower-case version of the episode.')
    # TODO: Runtime should be in youtube_video after using YouTube API. 
    # One few videos do not have YouTube id but does have runtime (videos never on YouTube).
    # nn:nn:nn (ex. 01:35:23 for 1hr 35min 23sec)
    runtime = models.CharField(max_length=11, blank=True, help_text='Enter episode runtime in format hh:mm:ss.')
    airdate = models.DateField(help_text='Enter original date the episode first aired.')

    # Metadata

    class Meta:
        ordering = ['-airdate']

    # Methods

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # test-chamber/test-chamber-title
        # shows/test-chamber/test-chamber-title
        # test-chamber-title
        return reverse('episode-detail-slug', kwargs={'slug': self.slug})

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

# class Heading(models.Model):
#     """Model representing a type of heading of an episode."""

#     # HEADING_TYPES = (
#     #     ('description', 'Description'),
#     #     ('gallery', 'Gallery'),
#     #     ('quotes', 'Quotes'),
#     # )

#     # Fields

#     title = models.CharField(max_length=100, help_text='Enter heading title.')

#     # Metadata
#     # Methods

#     def __str__(self):
#         return self.title

# # TODO: Different headings have different requirements. Description is just text, 
# # quotes should be formatted differently, gallery includes images, etc.
# class HeadingInstance(models.Model):
#     """Model representing a specific heading with different content."""

#     # Fields

#     heading = models.ForeignKey(Heading, on_delete=models.PROTECT, help_text='Enter heading type.')
#     #episode = models.ForeignKey('Episode', on_delete=models.CASCADE, help_text='Enter episode for which this heading instance belongs.')

#     # Metadata

#     class Meta:
#         verbose_name = 'Heading Instance'

#     # Methods
    
#     def __str__(self):
#         pass

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

# class YouTubeTag(models.Model):
#     """Model representing a YouTube video tag."""

#     # Fields

#     name = models.CharField(max_length=50, blank=True, help_text='Enter name of YouTube tag.')

#     # Metadata

#     class Meta:
#         verbose_name = 'YouTube Tag'

#     # Methods

#     def __str__(self):
#         return self.name

# TODO: Use YouTube Data API
class YouTubeVideo(models.Model):
    """Model representing a YouTube video."""

    # Fields

    youtube_id = models.CharField(max_length=15, blank=True, verbose_name='Video ID', help_text='Enter YouTube video ID.') # YouTube ID has 11 characters
    title = models.CharField(max_length=100, help_text='Enter title of the video.')
    views = models.PositiveBigIntegerField(null=True, blank=True, help_text='Enter number of views.')
    likes = models.PositiveIntegerField(null=True, blank=True, help_text='Enter number of likes.')
    dislikes = models.PositiveIntegerField(null=True, blank=True, help_text='Enter the number of dislikes.')
    thumbnails = models.ManyToManyField(Thumbnail, help_text='Enter thumbnail images for the video.')
    
    description = models.TextField(blank=True, help_text='Enter description of the video.')
    tags = models.JSONField(null=True, blank=True, help_text='Enter tags for the video.')
    duration = models.CharField(max_length=11, blank=True, help_text='Enter video duration in format: ex. PT1H34M35S.')
    published_at = models.DateField(null=True, blank=True, help_text='Enter date the YouTube video was published.')
    last_updated = models.DateField(auto_now=True)

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

    @property
    def duration_formatted(self):
        pattern = r'^PT(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?$'
        
        match = re.search(pattern, self.duration)
        if match is None:
            return None
            
        groups = list(match.groups())

        # Remove any None from beginning of groups tuple
        first_index_not_none = 0
        for index, match_group in enumerate(groups):
            if match_group is None:
                if first_index_not_none == index:
                    first_index_not_none += 1
                else: # Else first_index_not_none != index
                    groups[index] = '00'
            else: # match_group is not None
                if len(match_group) == 1 and first_index_not_none != index:
                    groups[index] = '0' + match_group

        return ':'.join(groups[slice(first_index_not_none, len(groups))])
