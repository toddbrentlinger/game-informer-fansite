from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

# Create your models here.
class CustomUser(AbstractUser):
    # Fields
    # Metadata
    # Methods

    def get_absolute_url(self):
        # users/5 -> User with id=5
        # users/toddbrentlinger -> User with username
        return reverse('customuser-detail', args=[str(self.id)])