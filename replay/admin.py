from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Article, ReplayEpisode, ReplaySeason, Segment, SegmentType

# Inlines

class ReplayEpisodeInline(admin.StackedInline):
    model = ReplayEpisode
    extra = 0

# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'datetime')
    list_filter = ('datetime',)
    search_fields = ['title', 'author__full_name', 'author__short_name']

@admin.register(ReplayEpisode)
class ReplayEpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'airdate')
    list_filter = ('airdate', 'season')
    #fields = ['number', ]
    filter_horizontal = ('featuring', 'external_links', 'main_segment_games', 'other_segments')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ReplaySeason)
class ReplaySeasonAdmin(admin.ModelAdmin):
    inlines = [ReplayEpisodeInline,]

@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):
    list_display = ('type', 'display_games')
    list_filter = ('type__abbreviation',)
    search_fields = ['games__title', 'description']
    filter_horizontal = ('games',)

@admin.register(SegmentType)
class SegmentTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'abbreviation')
    prepopulated_fields = {'slug': ('title',)}
