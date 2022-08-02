from django.db import models

from replay.models import YouTubeVideo

# Create your models here.

class Show(models.Model):
    # Fields

    name = models.CharField(max_length=100, help_text='Enter name of the show.')
    description = models.TextField(blank=True, help_text='Enter description of the show.')
    slug = models.SlugField(max_length=100, unique=True, null=False, help_text='Enter a url-safe, unique, lower-case version of the show.')

    # Metadata

    class Meta:
        ordering = ['name']

    # Methods
    
    def __str__(self):
        return self.name

class ShowEpisode(models.Model):
    # Fields

    show = models.ForeignKey(Show, on_delete=models.SET_NULL, blank=True, null=True, help_text='Enter show that includes the show episode.')
    slug = models.SlugField(max_length=100, unique=True, null=False, help_text='Enter a url-safe, unique, lower-case version of the show episode.')
    youtube_video = models.ForeignKey(YouTubeVideo, on_delete=models.CASCADE, help_text='Enter YouTube video of the show episode.')

    # Metadata
    # Methods

    def __str__(self):
        pass
