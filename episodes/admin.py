from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Episode, ExternalLink, Thumbnail, YouTubeVideo

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'airdate')
    filter_horizontal = ('featuring', 'external_links')

@admin.register(ExternalLink)
class ExternalLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    search_fields = ['title', 'url']

# @admin.register(Heading)
# class HeadingAdmin(admin.ModelAdmin):
#     inlines = [HeadingInstanceInline,]

# @admin.register(HeadingInstance)
# class HeadingInstanceAdmin(admin.ModelAdmin):
#     list_filter = ('heading__title',)

@admin.register(Thumbnail)
class ThumbnailAdmin(admin.ModelAdmin):
    list_filter = ('quality',)

@admin.register(YouTubeVideo)
class YouTubeVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_id', 'views', 'likes', 'dislikes')
    search_fields = ['title']
    filter_horizontal = ('thumbnails',)
