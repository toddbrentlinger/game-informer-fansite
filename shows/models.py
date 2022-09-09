from django.db import models
from django.urls import reverse

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

    def get_absolute_url(self):
        # test-chamber/
        # shows/test-chamber
        return reverse('show-detail-slug', kwargs={'slug': self.slug})

# TODO: 
# 9/8/22 - Remove unique attribute from slug field. Two ShowEpisodes can have 
# the same slug if the show is different. 
# Ex. test-chamber/dishonored and replay/dishonored
# ISSUE: If remove unique attribute from slug field, two ShowEpisodes in the 
# same Show could have the same slug. However, a unique slug is created inside 
# data migration script. Could just use that to make custom check whenever a 
# new ShowEpisode instance is created or updated.
# SOLUTION: Could instead remove slug field entirely and use pk value in it's place in 
# absolute url (ex. test-chamber/23).
# SOLUTION: Refactor slugify_unique function to only increment number on end 
# of slug when the Show is the same. Need to also remove unique attribute in 
# slug field.
class ShowEpisode(models.Model):
    # Fields

    show = models.ForeignKey(Show, on_delete=models.CASCADE, help_text='Enter show type of the episode.')
    episode = models.ForeignKey('episodes.Episode', on_delete=models.CASCADE, help_text='Enter episode.')
    slug = models.SlugField(max_length=100, unique=True, null=False, help_text='Enter a url-safe, unique, lower-case version of the show episode.')

    # Metadata
    # Methods

    def __str__(self):
        return f'{self.show} - {self.episode}'

    def get_absolute_url(self):
        # <show-slug>/<slug>
        # test-chamber/tomb-raider -> Episode: episodes/test-chamber-tomb-raider
        # replay/overblood -> Episode: episodes/replay-overblood
        # game-informer-show/most-anticipated-games-of-2022 -> Episode: episodes/most-anticipated-games-of-2022-gi-show
        return reverse('showepisode-detail-slug', kwargs={
            'show_slug': self.show.slug,
            'showepisode_slug': self.slug
        })
