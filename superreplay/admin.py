from django.contrib import admin
from .models import SuperReplay, SuperReplayEpisode

# Register your models here.

@admin.register(SuperReplay)
class SuperReplayAdmin(admin.ModelAdmin):
    pass