from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Thumbnail, YouTubeVideo, Person, Staff, StaffPosition, StaffPositionInstance, Article, SegmentType, Segment, ExternalLink, Heading, HeadingInstance, ReplaySeason, ReplayEpisode, SuperReplay, SuperReplayEpisode

# Inlines

class StaffPositionInstanceInline(admin.TabularInline):
    model = StaffPositionInstance
    extra = 0

class HeadingInstanceInline(admin.TabularInline):
    model = HeadingInstance
    extra = 0

class ReplayEpisodeInline(admin.StackedInline):
    model = ReplayEpisode
    extra = 0

class SuperReplayEpisodeInline(admin.StackedInline):
    model = SuperReplayEpisode
    extra = 0

# Register your models here.

@admin.register(Thumbnail)
class ThumbnailAdmin(admin.ModelAdmin):
    list_filter = ('quality',)

@admin.register(YouTubeVideo)
class YouTubeVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_id', 'views', 'likes', 'dislikes')
    search_fields = ['title']

# @admin.register(Game)
# class GameAdmin(admin.ModelAdmin):
#     list_display = ('title', 'system', 'release_year')
#     list_filter = ('system', 'release_year')
#     search_fields = ['title']

# @admin.register(Guest)
# class GuestAdmin(admin.ModelAdmin):
#     search_fields = ['first_name', 'last_name']

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass

@admin.register(StaffPosition)
class StaffPositionAdmin(admin.ModelAdmin):
    search_fields = ['title']
    inlines = [StaffPositionInstanceInline,]

@admin.register(StaffPositionInstance)
class StaffPositionInstanceAdmin(admin.ModelAdmin):
    list_filter = ('position__title',)
    search_fields = ['staff__person__full_name', 'staff__person__short_name', 'position__title']

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    search_fields = ['person__full_name']
    inlines = [StaffPositionInstanceInline,]

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'datetime')
    list_filter = ('datetime',)
    search_fields = ['title', 'author__full_name', 'author__short_name']

@admin.register(SegmentType)
class SegmentTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'abbreviation')

@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):
    list_display = ('type', 'display_games')
    list_filter = ('type__abbreviation',)
    search_fields = ['games__title', 'description']
    filter_horizontal = ('games',)

@admin.register(ExternalLink)
class ExternalLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    search_fields = ['title', 'url']

@admin.register(Heading)
class HeadingAdmin(admin.ModelAdmin):
    inlines = [HeadingInstanceInline,]

@admin.register(HeadingInstance)
class HeadingInstanceAdmin(admin.ModelAdmin):
    list_filter = ('heading__title',)

@admin.register(ReplaySeason)
class ReplaySeasonAdmin(admin.ModelAdmin):
    inlines = [ReplayEpisodeInline,]

@admin.register(ReplayEpisode)
class ReplayEpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'airdate')
    list_filter = ('airdate', 'season')
    #fields = ['number', ]
    filter_horizontal = ('featuring', 'external_links', 'main_segment_games', 'other_segments')

@admin.register(SuperReplay)
class SuperReplayAdmin(admin.ModelAdmin):
    inlines = [SuperReplayEpisodeInline,]

@admin.register(SuperReplayEpisode)
class SuperReplayEpisodeAdmin(admin.ModelAdmin):
    pass