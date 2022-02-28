from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Thumbnail, YouTubeVideo, Guest, StaffPosition, StaffPositionInstance, Staff, Article, SegmentType, Segment, ExternalLink, Heading, HeadingInstance, ReplaySeason, ReplayEpisode, SuperReplay, SuperReplayEpisode

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

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']

class StaffPositionInstanceInline(admin.TabularInline):
    model = StaffPositionInstance

@admin.register(StaffPosition)
class StaffPositionAdmin(admin.ModelAdmin):
    search_fields = ['title']
    inlines = [StaffPositionInstanceInline,]

@admin.register(StaffPositionInstance)
class StaffPositionInstanceAdmin(admin.ModelAdmin):
    list_filter = ('position__title',)
    search_fields = ['staff__first_name', 'staff__last_name', 'position__title']

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']
    inlines = [StaffPositionInstanceInline,]

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'datetime')
    list_filter = ('datetime',)
    search_fields = ['title', 'author__first_name', 'author__last_name']

@admin.register(SegmentType)
class SegmentTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'abbreviation')

@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):
    list_filter = ('type__abbreviation',)
    search_fields = ['games__title', 'description']

@admin.register(ExternalLink)
class ExternalLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    search_fields = ['title', 'url']

class HeadingInstanceInline(admin.TabularInline):
    model = HeadingInstance

@admin.register(Heading)
class HeadingAdmin(admin.ModelAdmin):
    inlines = [HeadingInstanceInline,]

@admin.register(HeadingInstance)
class HeadingInstanceAdmin(admin.ModelAdmin):
    list_filter = ('heading__title',)

class ReplayEpisodeInline(admin.TabularInline):
    model = ReplayEpisode

@admin.register(ReplaySeason)
class ReplaySeasonAdmin(admin.ModelAdmin):
    inlines = [ReplayEpisodeInline,]

@admin.register(ReplayEpisode)
class ReplayEpisodeAdmin(admin.ModelAdmin):
    list_filter = ('airdate',)
    #fields = ['number', ]
    filter_horizontal = ('thumbnails', 'featuring', 'guests')

class SuperReplayEpisodeInline(admin.TabularInline):
    model = SuperReplayEpisode

@admin.register(SuperReplay)
class SuperReplayAdmin(admin.ModelAdmin):
    inlines = [SuperReplayEpisodeInline,]

@admin.register(SuperReplayEpisode)
class SuperReplayEpisodeAdmin(admin.ModelAdmin):
    pass