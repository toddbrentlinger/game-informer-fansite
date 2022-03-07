from django.contrib import admin
from .models import Genre, Developer, PlatformLogo, Platform, Game

# Register your models here.

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    pass

@admin.register(PlatformLogo)
class PlatformLogoAdmin(admin.ModelAdmin):
    pass

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    pass

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'platform', 'release_date')
    list_filter = ('platform__abbreviation', 'release_date')
    search_fields = ['name']