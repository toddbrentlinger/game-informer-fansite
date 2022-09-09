from django.contrib import admin
from .models import Show, ShowEpisode

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    pass

@admin.register(ShowEpisode)
class ShowEpisodeAdmin(admin.ModelAdmin):
    pass
