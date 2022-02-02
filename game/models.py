from django.db import models
from django.urls import reverse

# Create your models here.

class Genre(models.Model):
    # Fields
    # Metadata
    # Methods
    pass

class Developer(models.Model):
    # Fields
    # Metadata
    # Methods
    pass

class System(models.Model):
    # Fields
    # Metadata
    # Methods
    pass

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
        return f'{self.title} [{self.get_system_display()}]'

    # TODO: Use IGDB API to display information about the game as well as any stored
    # fields (ex. other episodes that include that game)
    def get_absolute_url(self):
        # game/metal-gear-solid-3
        pass