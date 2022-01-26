from django.contrib import admin
from .models import Thumbnail, YouTubeVideo, Game, Guest, StaffRole, Staff, Article, Segment, SegmentInstance, ExternalLink, Heading, HeadingInstance, ReplayEpisode, SuperReplay, SuperReplayEpisode

# Register your models here.
admin.site.register(Thumbnail)
admin.site.register(YouTubeVideo)
admin.site.register(Game)
admin.site.register(Guest)
admin.site.register(StaffRole)
admin.site.register(Staff)
admin.site.register(Article)
admin.site.register(Segment)
admin.site.register(SegmentInstance)
admin.site.register(ExternalLink)
admin.site.register(Heading)
admin.site.register(HeadingInstance)
admin.site.register(ReplayEpisode)
admin.site.register(SuperReplay)
admin.site.register(SuperReplayEpisode)