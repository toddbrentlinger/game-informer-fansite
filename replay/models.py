import uuid # used for unique model instances
import re

from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from games.models import Game
from people.models import Person
from shows.models import ShowEpisode
#from episodes.models import Episode

# Create your models here.

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

# TODO: Replace 'middle_segment' and 'second_segment' with 'segments' ManyToManyField.
# Should add main segment inside segments instead of having separate field just for main segment games?
class ReplayEpisode(models.Model):
    """Model representing an episode of Replay."""

    # Fields

    show_episode = models.OneToOneField(ShowEpisode, on_delete=models.PROTECT, help_text='Enter show episode for the Replay episode.')
    season = models.ForeignKey('ReplaySeason', on_delete=models.CASCADE, verbose_name='Replay Season', help_text='Enter season of the Replay episode.')
    number = models.SmallIntegerField(unique=True, help_text='Enter Replay episode number (unofficial episodes use negative numbers).')
    main_segment_games = models.ManyToManyField(Game, verbose_name='Main Segment Games', help_text='Enter any games part of the main segment of the Replay episode.')
    other_segments = models.ManyToManyField('Segment', blank=True, verbose_name='Other Segments', help_text='Enter other segments for the Replay episode.')
    # middle_segment = models.ForeignKey(Segment, related_name='%(app_label)s_%(class)s_middle_segment_related', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Middle Segment', help_text='Enter middle segment for the Replay episode.')
    # second_segment = models.ForeignKey(Segment, related_name='%(app_label)s_%(class)s_second_segment_related', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Second Segment', help_text='Enter second segment for the Replay episode.')
    article = models.OneToOneField(Article, on_delete=models.SET_NULL, null=True, blank=True, help_text='Enter article for the Replay episode.')

    # Metadata

    class Meta:
        verbose_name = 'Replay Episode'

    # Methods
    
    def __str__(self):
        return f'{ self.show_episode } (S{ self.season }:E{ self.number })'

    def get_absolute_url(self):
        # replay/378 -> Replay Episode 378
        # replay/s2/45 -> Replay Season 2 Episode 45
        # replay/metal-gear-solid-3
        return reverse('replay-detail-slug', kwargs={'slug': self.show_episode.slug})
        #return reverse('replay-detail', args=[str(self.id)])

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(re.sub(r'Replay:\s?', '', self.title, 1, re.IGNORECASE))
    #     return super(ReplayEpisode, self).save(*args, **kwargs)

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
        return reverse('segment-type-detail-slug', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(SegmentType, self).save(*args, **kwargs)
