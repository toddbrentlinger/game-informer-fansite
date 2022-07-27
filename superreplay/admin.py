from django.contrib import admin
from .models import SuperReplay, SuperReplayEpisode, SuperReplayGame

# Register your models here.

@admin.register(SuperReplay)
class SuperReplayAdmin(admin.ModelAdmin):
    pass

@admin.register(SuperReplayEpisode)
class SuperReplayEpisodeAdmin(admin.ModelAdmin):
    pass

@admin.register(SuperReplayGame)
class SuperReplayGameAdmin(admin.ModelAdmin):
    pass