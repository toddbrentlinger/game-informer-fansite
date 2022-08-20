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
