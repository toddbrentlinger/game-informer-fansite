from django.db import models
from django.urls import reverse
from replay.models import Episode

# Create your models here.

class SuperReplay(models.Model):
    """Model representing a Super Replay."""

    # Fields

    slug = models.SlugField(max_length=100, unique=True, null=False)

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