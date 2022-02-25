from django.db import models
from django.urls import reverse

# Create your models here.

class Genre(models.Model):
    # Fields
    id = models.PositiveSmallIntegerField(primary_key=True, help_text='Enter IGDB ID for this genre.')
    name = models.CharField(max_length=200, help_text='Enter name of this genre.')
    
    # Metadata
    class Meta:
        ordering = ['id']
    
    # Methods
    def __str__(self):
        return self.name

class Developer(models.Model):
    # Fields
    # Metadata
    # Methods
    pass

class PlatformLogo(models.Model):
    # Fields

    # Metadata
    # Methods
    pass

class Platform(models.Model):
    # Fields
    id = models.PositiveSmallIntegerField(primary_key=True, help_text='Enter IGDB ID for this system/platform.')
    abbreviation = models.CharField(max_length=20, help_text='Enter shortened abbreviation for this system/platform.')
    alternate_name = models.CharField(max_length=1000, help_text='Enter alternate names as list separated by commas.')
    name = models.CharField(max_length=200, help_text='Enter name of this system/platform.')
    logo = models.ForeignKey(PlatformLogo, null=True, blank=True, help_text='Enter logo for this system/platform.')

    # Metadata
    class Meta:
        ordering = ['id']

    # Methods
    def __str__(self):
        return self.name

# TODO: Use VGDB (Video Game Database API)
# - *Could use API to fill a few basic fields to be stored on custom database and 
# use API whenever user accesses custom page for single game (ex. /game/metal-gear-solid-3)
# Which fields to store on custom database? (fields to sort/filter by)
#   -   Title, System, Release Date, Developer, Genres
# - Game model should hold system they played the game on since the IGDB shows all platforms per game ID,
# however IGDB displays separate release dates per system.
class Game(models.Model):
    """Model representing a video game."""

    # Fields

    igdb_id = models.PositiveIntegerField(null=True, blank=True, verbose_name='IGDB ID', help_text='Enter IGDB game ID to be used with API. If ID entered, other fields do NOT need to be filled out.')
    #title = models.CharField(max_length=200, help_text='Enter game title.')
    #system = models.CharField(max_length=50, help_text='Enter game system (ex. PC, PS4, XBox 360, etc.).')
    release_year = models.PositiveSmallIntegerField(verbose_name='Release Year', help_text='Enter year the game was released.')

    name = models.CharField(max_length=200, help_text='Enter game title.')
    slug = models.SlugField(max_length=200)
    platform = models.ForeignKey(Platform, help_text='Enter game platform (ex. PC, PS4, XBox 360, etc.).')
    genre = models.ManyToManyField(Genre, blank=True, help_text='Enter genres of the game.')
    developer = models.ForeignKey(Developer, null=True, blank=True, on_delete=models.SET_NULL, help_text='Enter developer of the game.')
    release_date = models.DateField(verbose_name='Release Date', help_text='Enter date the game was released.')

    # Metadata

    class Meta:
        ordering = ['name', 'release_year']

    # Methods

    def __str__(self):
        return f'{self.name} [{self.platform}]'

    # TODO: Use IGDB API to display information about the game as well as any stored
    # fields (ex. other episodes that include that game)
    # - Append slug field to "game/"
    def get_absolute_url(self):
        # game/metal-gear-solid-3
        pass

    def save(self, *args, **kwargs):
        super(Game, self).save(*args, **kwargs)