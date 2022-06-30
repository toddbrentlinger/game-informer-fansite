from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

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

class ImageIGDB(models.Model):
    # Fields
    igdb_id = models.CharField(max_length=100, help_text='Enter the ID of the image used to construct an IGDB image link.')
    width = models.PositiveSmallIntegerField(help_text='Enter the width of the image in pixels.')
    height = models.PositiveSmallIntegerField(help_text='Enter the height of the image in pixels.')
    url = models.URLField(help_text='Enter the IGDB website address (URL) of the image.')

    # Metadata

    class Meta:
        ordering = ['igdb_id']
        verbose_name = 'Image'

    # Methods
    def __str__(self):
        return self.igdb_id

class Platform(models.Model):
    # Fields
    id = models.PositiveSmallIntegerField(primary_key=True, help_text='Enter IGDB ID of the system/platform.')
    name = models.CharField(max_length=200, help_text='Enter name of this system/platform.')
    abbreviation = models.CharField(max_length=20, blank=True, help_text='Enter shortened abbreviation for this system/platform.')
    alternative_name = models.CharField(max_length=1000, blank=True, help_text='Enter alternative names as list separated by commas.')
    logo = models.ForeignKey(ImageIGDB, on_delete=models.SET_NULL, null=True, blank=True, help_text='Enter logo of the first Version of this platform.')
    slug = models.SlugField(max_length=200, unique=True, null=False, help_text='Enter a url-safe, unique, lower-case version of the platform.')
    summary = models.TextField(blank=True, help_text='Enter a summary of the first Version of this platform.')
    url = models.URLField(help_text='Enter the IGDB website address (URL) of the platform.')

    # Metadata
    class Meta:
        ordering = ['name']

    # Methods
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('platform-detail-slug', kwargs={'stub': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Platform, self).save(*args, **kwargs)

class Developer(models.Model):
    # Fields
    id = models.PositiveIntegerField(primary_key=True, help_text='Enter IGDB ID of the company.')
    name = models.CharField(max_length=200, help_text='Enter name of the company.')
    country = models.PositiveSmallIntegerField(blank=True, null=True, help_text='Enter the ISO 3166-1 country code.')
    description = models.TextField(blank=True, help_text='Enter free text description of the company.')
    logo = models.ForeignKey(ImageIGDB, on_delete=models.SET_NULL, null=True, blank=True, help_text='Enter logo of the company.')
    slug = models.SlugField(max_length=200, unique=True, null=False, help_text='Enter a url-safe, unique, lower-case version of the company.')
    url = models.URLField(help_text='Enter the IGDB website address (URL) of the company.')

    # Metadata
    class Meta:
        ordering = ['name']

    # Methods
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('developer-detail-slug', kwargs={'stub': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Developer, self).save(*args, **kwargs)

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
    name = models.CharField(max_length=200, help_text='Enter game title.')
    slug = models.SlugField(max_length=200, unique=True, null=False)
    summary = models.TextField(blank=True, help_text='Enter description of the game.')
    storyline = models.TextField(blank=True, help_text='Enter short description of the game\'s story.')
    platform = models.ForeignKey(Platform, on_delete=models.SET_NULL, null=True, blank=True, help_text='Enter game platform (ex. PC, PS4, XBox 360, etc.).')
    genres = models.ManyToManyField(Genre, blank=True, help_text='Enter genres of the game.')
    developer = models.ForeignKey(Developer, on_delete=models.SET_NULL, null=True, blank=True, help_text='Enter developer of the game.')
    release_date = models.DateTimeField(blank=True, null=True, verbose_name='Release Date', help_text='Enter date the game was released.')
    cover = models.OneToOneField(ImageIGDB, on_delete=models.SET_NULL, null=True, blank=True, help_text='Enter the cover of the game.')
    #screenshots = models.ManyToManyField(ImageIGDB, blank=True, help_text='Enter screenshots of the game.')
    url = models.URLField(blank=True, help_text='Enter the IGDB website address (URL) of the game.')

    # Metadata

    class Meta:
        ordering = ['name', 'release_date']

    # Methods

    def __str__(self):
        output_str = self.name
        if self.platform is not None:
            output_str += f' ({self.platform.abbreviation})'
        return output_str

    # TODO: Use IGDB API to display information about the game as well as any stored
    # fields (ex. other episodes that include that game)
    # - Append slug field to "game/"
    def get_absolute_url(self):
        # game/metal-gear-solid-3
        return reverse('game-detail-slug', kwargs={'stub': self.slug})
        #return reverse('game-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Game, self).save(*args, **kwargs)