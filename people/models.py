from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
#from fansite.models import Thumbnail

# Create your models here.

# TODO: Use Person as normal class for guests since there's no extra functionality for Guest over generic Person class.
# However, do want separate detail page for guests and staff members.
# class Guest(Person):
#     """Model representing a guest (not staff member)."""

#     # Fields
#     # Metadata
#     # # Methods

#     def get_absolute_url(self):
#         # guests/hilary-wilton
#         pass

class Person(models.Model):
    """Model representing a person."""

    # Fields

    full_name = models.CharField(max_length=100, verbose_name='Full Name', help_text='Enter full name (maximum 100 characters).')
    short_name = models.CharField(max_length=50, blank=True, verbose_name='Short Name', help_text='Enter optional short name variation for usage in correspondence (maximum 50 characters).')
    slug = models.SlugField(max_length=100, unique=True, null=False)
    description = models.TextField(blank=True)
    headings = models.JSONField(null=True, blank=True, help_text='Enter JSON of different headings with key being the heading title and value being the content.')
    thumbnail = models.ForeignKey('fansite.Thumbnail', on_delete=models.SET_NULL, null=True, blank=True)
    infobox_details = models.JSONField(null=True, blank=True, help_text='Enter JSON of different headings with key being the heading title and value being the content.')

    # gallery 
    # trivia
    # social_media: Inside SocialMediaInst, person = models.ForeignKey(Person)

    # Metadata

    class Meta:
        ordering = ['full_name']
        verbose_name_plural = 'people'

    # Methods

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        # staff/andrew-reiner
        # staff/tim-turi
        # guests/hilary-wilton
        # people/tim-turi
        return reverse('person-detail-slug', kwargs={'stub': self.slug})
        #return reverse('people', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name)
        return super(Person, self).save(*args, **kwargs)

# Each model represents Facebook, Twitter, etc.
# Can use separate API to request certain data, ex. recent tweets from twitter account listed in SocialMediaInst.
class SocialMediaInst(models.Model):
    # Fields

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    url = models.URLField()

    # Metadata
    # Methods

    def __str__(self):
        return f'{self.person} ({self.type})'

# TODO: Use 'Extra fields on many-to-many relationships' for roles, creating an 
# intermediate class RoleDuration to hold start_date, end_date, and anything else. 
class Staff(models.Model):
    """Model representing a staff member."""

    # Fields

    person = models.OneToOneField(Person, on_delete=models.CASCADE)

    # Metadata

    class Meta:
        verbose_name = 'Staff Member'
        verbose_name_plural = 'Staff'

    # Methods

    def __str__(self):
        return str(self.person)

    # def get_absolute_url(self):
    #     # staff/andrew-reiner
    #     # staff/tim-turi
    #     return reverse('staff', args=[str(self.id)])

class StaffPosition(models.Model):
    """Model representing a specific position at the company."""

    # Fields

    title = models.CharField(max_length=200, help_text='Enter title of position.')

    # Metadata

    class Meta:
        ordering = ['title']
        verbose_name = 'Staff Position'

    # Methods

    def __str__(self):
        return self.title

# TODO: Add validator to check end_date is greater than start_date
# TODO: Convert to StaffRole and intermediate class StaffRoleDuration (see Staff)
class StaffPositionInstance(models.Model):
    """Model representing a single instance of a position at the company."""

    # Fields

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, help_text='Enter staff member for this position instance.')
    position = models.ForeignKey(StaffPosition, on_delete=models.PROTECT, help_text='Enter position of the staff member.')
    start_year = models.PositiveSmallIntegerField(verbose_name='Start Year', help_text='Enter date started the position.')
    end_year = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='End Year', help_text='Enter date started the position.')

    # Metadata

    class Meta:
        ordering = ['-start_year']
        verbose_name = 'Staff Position Instance'

    # Methods

    def __str__(self):
        return f'{self.position} [{self.start_date} - {self.end_date}]'