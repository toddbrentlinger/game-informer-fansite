from django.contrib import admin
from .models import Artwork, Collection, Developer, Franchise, Game, GameVideo, Genre, ImageIGDB, Keyword, Platform, Screenshot, Theme, Website

# Register your models here.

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    pass

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    pass

@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Franchise)
class FranchiseAdmin(admin.ModelAdmin):
    pass

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'release_date')
    list_filter = ('platforms__abbreviation', 'release_date')
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(GameVideo)
class GameVideoAdmin(admin.ModelAdmin):
    pass

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

@admin.register(ImageIGDB)
class PlatformLogoAdmin(admin.ModelAdmin):
    pass

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    pass

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation', 'id')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Screenshot)
class ScreenshotAdmin(admin.ModelAdmin):
    pass

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    pass

@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    pass