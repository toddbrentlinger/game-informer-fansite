from django.db import models
from django.urls import reverse
from replay.models import Episode

# Create your models here.

class SuperReplay(models.Model):
    '''Model representing a Super Replay.'''

    # Fields

    title = models.CharField(max_length=100, help_text='Enter title of the super replay.')
    number = models.SmallIntegerField(unique=True, help_text='Enter Super Replay number (unofficial Super Replays use negative numbers).')
    article = models.OneToOneField('replay.Article', on_delete=models.SET_NULL, null=True, blank=True, help_text='Enter article for the Super Replay.')
    headings = models.JSONField(null=True, blank=True, help_text='Enter JSON of different headings with key being the heading title and value being the content.')
    external_links = models.ManyToManyField('replay.ExternalLink', blank=True, verbose_name='External Links', help_text='Enter any external URL links (NOT including Game Informer article OR YouTube video).')
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
    '''Model representing an episode of Super Replay.'''

    # Fields

    # Fields from Episode not needed (put in child model ReplayEpisode):
    # title, slug

    super_replay = models.ForeignKey(SuperReplay, on_delete=models.CASCADE, help_text='Enter Super Replay for this episode.')
    episode_number = models.PositiveSmallIntegerField(help_text='Enter episode number in the Super Replay.')

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

class SuperReplayGame(models.Model):
    '''Model representing a game played on a Super Replay.'''

    # Fields

    super_replay = models.ForeignKey(SuperReplay, on_delete=models.CASCADE, help_text='Enter Super Replay in which the game was played.')
    game = models.OneToOneField('games.Game', on_delete=models.CASCADE, help_text='Enter game played in the Super Replay.')

    # Metadata

    # Methods

    def __str__(self):
        return f'${self.game.name} (${self.super_replay.title})'