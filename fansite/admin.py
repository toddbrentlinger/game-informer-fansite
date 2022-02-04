from django.contrib import admin
from .models import Thumbnail, YouTubeVideo, Game, Guest, StaffPosition, StaffPositionInstance, Staff, Article, SegmentType, Segment, ExternalLink, Heading, HeadingInstance, ReplayEpisode, SuperReplay, SuperReplayEpisode

# Register your models here.
admin.site.register(Thumbnail)
#admin.site.register(YouTubeVideo)
admin.site.register(Game)
#admin.site.register(Guest)
admin.site.register(StaffPosition)
admin.site.register(StaffPositionInstance)
#admin.site.register(Staff)
#admin.site.register(Article)
admin.site.register(SegmentType)
#admin.site.register(Segment)
#admin.site.register(ExternalLink)
admin.site.register(Heading)
admin.site.register(HeadingInstance)
admin.site.register(ReplayEpisode)
admin.site.register(SuperReplay)
admin.site.register(SuperReplayEpisode)

@admin.register(YouTubeVideo)
class YouTubeVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_id', 'views', 'likes', 'dislikes')

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    pass

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    pass

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'datetime')

@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):
    list_display = ('segment_type', 'display_games')

@admin.register(ExternalLink)
class ExternalLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')