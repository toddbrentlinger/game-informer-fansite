from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

# Abstract Models

class BaseIGDB(models.Model):
    """Abstract model representing a base IGDB model."""

    # Fields

    id = models.PositiveIntegerField(primary_key=True, help_text='Enter IGDB ID of the item.')
    name = models.CharField(max_length=200, help_text='Enter name of the item.')
    slug = models.SlugField(max_length=200, unique=True, null=False, help_text='Enter a url-safe, unique, lower-case version of the item.')
    url = models.URLField(blank=True, help_text='Enter the IGDB website address (URL) of the item.')
    
    # Metadata

    class Meta:
        abstract = True
        ordering = ['name']
    
    # Methods

    def __str__(self):
        return self.name

# TODO: If game is deleted, screenshot is deleted, but ImageIGDB remains in database. Add method to handle
# removing the ImageIGDB from the database if screenshot is deleted.
class ImageType(models.Model):
    """Abstract model representing a type of ImageIGDB (ex. screenshot, artwork, etc.)."""

    # Fields

    # id = models.PositiveIntegerField(primary_key=True, help_text='Enter IGDB ID of the IGDB image.')
    image = models.OneToOneField('ImageIGDB', on_delete=models.CASCADE, help_text='Enter the IGDB Image.')
    game = models.ForeignKey('Game', on_delete=models.CASCADE, help_text='Enter the game.')

    # Metadata

    class Meta:
        abstract = True

    # Methods

    def __str__(self):
        return f'{self.image.image_id} - {self.game.name}'

class SeriesBase(BaseIGDB):
    """Abstract model representing a video game collection/series/franchise."""

    # Fields

    games = models.ManyToManyField('Game', help_text='Enter games associated with the item.')

    # Metadata

    class Meta(BaseIGDB.Meta):
        abstract = True

    # Methods

# Create your models here.

class Artwork(ImageType):
    """Model representing a video game artwork."""

    # Fields
    # Metadata
    # Methods
    pass

class Collection(SeriesBase):
    """Model representing a video game collection."""

    # Fields
    # Metadata

    # Methods

    def get_absolute_url(self):
        return reverse('collection-detail-slug', kwargs={'slug': self.slug})

class Developer(BaseIGDB):
    """Model representing a video game developer."""

    # Fields

    country = models.PositiveSmallIntegerField(blank=True, null=True, help_text='Enter the ISO 3166-1 country code.')
    description = models.TextField(blank=True, help_text='Enter free text description of the company.')
    logo = models.ForeignKey('ImageIGDB', on_delete=models.SET_NULL, null=True, blank=True, help_text='Enter logo of the company.')

    # Metadata

    # Methods

    def get_absolute_url(self):
        return reverse('developer-detail-slug', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Developer, self).save(*args, **kwargs)

class Franchise(SeriesBase):
    """Model representing a video game franchise."""

    # Fields
    # Metadata

    # Methods

    def get_absolute_url(self):
        return reverse('franchise-detail-slug', kwargs={'slug': self.slug})

# TODO: Use VGDB (Video Game Database API)
# - *Could use API to fill a few basic fields to be stored on custom database and 
# use API whenever user accesses custom page for single game (ex. /game/metal-gear-solid-3)
# Which fields to store on custom database? (fields to sort/filter by)
#   -   Title, System, Release Date, Developer, Genres
# - Game model should hold system they played the game on since the IGDB shows all platforms per game ID,
# however IGDB displays separate release dates per system.
class Game(BaseIGDB):
    """Model representing a video game."""

    # Fields

    #igdb_id = models.PositiveIntegerField(null=True, blank=True, verbose_name='IGDB ID', help_text='Enter IGDB game ID to be used with API. If ID entered, other fields do NOT need to be filled out.')
    summary = models.TextField(blank=True, help_text='Enter description of the game.')
    storyline = models.TextField(blank=True, help_text='Enter short description of the game\'s story.')
    platform = models.ForeignKey('Platform', on_delete=models.SET_NULL, null=True, blank=True, help_text='Enter game platform (ex. PC, PS4, XBox 360, etc.).')
    genres = models.ManyToManyField('Genre', blank=True, help_text='Enter genres of the game.')
    keywords = models.ManyToManyField('Keyword', blank=True, help_text='Enter keywords of the game.')
    themes = models.ManyToManyField('Theme', blank=True, help_text='Enter themes of the game.')
    developer = models.ForeignKey(Developer, on_delete=models.SET_NULL, null=True, blank=True, help_text='Enter developer of the game.')
    release_date = models.DateTimeField(blank=True, null=True, verbose_name='Release Date', help_text='Enter date the game was released.')
    cover = models.OneToOneField('ImageIGDB', on_delete=models.SET_NULL, null=True, blank=True, help_text='Enter the cover of the game.')
    websites = models.ManyToManyField('Website', blank=True, help_text='Enter websites associated with the game.')


    # Metadata

    class Meta(BaseIGDB.Meta):
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
        return reverse('game-detail-slug', kwargs={'slug': self.slug})
        #return reverse('game-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Game, self).save(*args, **kwargs)

class GameVideo(models.Model):
    """Model representing a video game video."""

    # Fields

    id = models.PositiveIntegerField(primary_key=True, help_text='Enter IGDB ID of the video.')
    name = models.CharField(max_length=200, blank=True, help_text='Enter the name of the video.')
    video_id = models.CharField(max_length=50, help_text='Enter the external ID of the video (usually YouTube).')
    game = models.ForeignKey('Game', on_delete=models.CASCADE, help_text='Enter the game.')

    # Metadata

    class Meta:
        pass

    # Methods

    def __str__(self):
        return f'{self.name} [ID: {self.video_id} - Game: {self.game.name}]'

class Genre(BaseIGDB):
    """Model representing a video game genre."""

    # Fields
    # Metadata
    
    # Methods

    def get_absolute_url(self):
        return reverse('genre-detail-slug', kwargs={'slug': self.slug})

class ImageIGDB(models.Model):
    """Model representing a video game image from IGDB."""

    # Fields

    id = models.PositiveIntegerField(primary_key=True, help_text='Enter IGDB ID of the image.')
    image_id = models.CharField(max_length=100, help_text='Enter the ID of the image used to construct an IGDB image link.')
    width = models.PositiveSmallIntegerField(blank=True, null=True, help_text='Enter the width of the image in pixels.')
    height = models.PositiveSmallIntegerField(blank=True, null=True, help_text='Enter the height of the image in pixels.')

    # Metadata

    class Meta:
        ordering = ['id']
        verbose_name = 'Image'

    # Methods

    def __str__(self):
        return self.image_id

class Keyword(BaseIGDB):
    """Model representing a video game keyword."""

    # Fields
    # Metadata

    # Methods
    
    def get_absolute_url(self):
        return reverse('keyword-detail-slug', kwargs={'slug': self.slug})

class Platform(BaseIGDB):
    """Model representing a video game platform."""

    # Fields

    abbreviation = models.CharField(max_length=20, blank=True, help_text='Enter shortened abbreviation for this system/platform.')
    alternative_name = models.CharField(max_length=1000, blank=True, help_text='Enter alternative names as list separated by commas.')
    logo = models.ForeignKey(ImageIGDB, on_delete=models.SET_NULL, null=True, blank=True, help_text='Enter logo of the first Version of this platform.')
    summary = models.TextField(blank=True, help_text='Enter a summary of the first Version of this platform.')

    # Metadata

    # Methods

    def get_absolute_url(self):
        return reverse('platform-detail-slug', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Platform, self).save(*args, **kwargs)

class Screenshot(ImageType):
    """Model representing a video game screenshot."""

    # Fields
    # Metadata
    # Methods
    pass

class Theme(BaseIGDB):
    """Model representing a video game theme."""

    # Fields
    # Metadata

    # Methods
    
    def get_absolute_url(self):
        return reverse('theme-detail-slug', kwargs={'slug': self.slug})

class Website(models.Model):
    """Model representing a video game website."""

    class WebsiteType(models.IntegerChoices):
        OFFICIAL = 1
        WIKIA = 2
        WIKIPEDIA = 3
        FACEBOOK = 4
        TWITTER = 5
        TWITCH = 6
        INSTAGRAM = 8
        YOUTUBE = 9
        IPHONE = 10
        IPAD = 11
        ANDROID = 12
        STEAM = 13
        REDDIT = 14
        ITCH = 15
        EPICGAMES = 16
        GOG = 17
        DISCORD = 18

    # Fields

    category = models.PositiveSmallIntegerField(choices=WebsiteType.choices)
    trusted = models.BooleanField(default=False)
    url = models.URLField(help_text='Enter the IGDB website address (URL) of the item.')

    # Metadata

    # Methods

    def __str__(self):
        return f'{self.category} - {self.url}'