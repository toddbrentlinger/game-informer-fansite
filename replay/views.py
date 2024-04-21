from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views import generic
from .models import ReplayEpisode, SegmentType
from episodes.views import creat_sort_filter_context
from random import choice

# Utility Functions

def creat_sort_filter_context_replay(request, query_set):
    # Add 'replay' sort option that sorts ReplayEpisodes by replay episode number.
    # Also add 'show_episode__episode__' prefix to sort options that reference base Episode fields.
    SORT_UPDATES = {
        'replay': 'number',
        'airdate': 'show_episode__episode__airdate',
        'likes': 'show_episode__episode__youtube_video__likes',
        'video-length': 'show_episode__episode__youtube_video__duration',
        'views': 'show_episode__episode__youtube_video__views',
    }

    # Create base context to display list passing in request, query_set, 
    # SORT_UPDATES for this app, and to sort by ReplayEpisode number by 
    # default.
    return creat_sort_filter_context(
        request, 
        query_set, 
        '',
        SORT_UPDATES, 
        'replay'
    )

# Replay List View

def replay_episode_list_view(request):
    """Return HttpResponse to display list of ReplayEpisodes that are filtered and sorted depending on request."""
    # Create base context to display list passing in all ReplayEpisodes as the 
    # QuerySet.
    context = creat_sort_filter_context_replay(
        request, 
        ReplayEpisode.objects.all(), 
    )
    
    return render(request, 'replay/replayepisode_list.html', context=context)

# ReplayEpisode Detail Views

def replay_episode_detail_view_base(request, replayepisode):
    """Return HttpResponse to display single ReplayEpisode detail, given ReplayEpisode."""
    context = {
        'episode': replayepisode.show_episode.episode,
        'replayepisode': replayepisode
    }

    return render(request, 'replay/replayepisode_detail.html', context=context)

def replay_episode_detail_view(request, pk):
    """Return HttpResponse to display single ReplayEpisode detail, given ReplayEpisode, given primary key for specific ReplayEpisode."""
    replayepisode = get_object_or_404(ReplayEpisode, pk=pk)
    return replay_episode_detail_view_base(request, replayepisode)

def replay_episode_detail_season_episode_view(request, season, number):
    """Return HttpResponse to display single ReplayEpisode detail, given season and season episode for specific ReplayEpisode."""
    # Use custom Manager in ReplayEpisode to find ReplayEpisode with season and season episode number
    replayepisode = ReplayEpisode.objects.with_season_and_episode(season, number)
    return replay_episode_detail_view_base(request, replayepisode)

def replay_episode_detail_slug_view(request, slug):
    """Return HttpResponse to display single ReplayEpisode detail, given slug for specific ReplayEpisode."""
    replayepisode = get_object_or_404(ReplayEpisode, show_episode__slug=slug)
    return replay_episode_detail_view_base(request, replayepisode)

# Replay Segment Views

def segment_type_list_view(request):
    """Return a HttpResponse to display list of Replay segments."""
    # Create QuerySet of all segments
    segmenttype_list = SegmentType.objects.all()

    # Create Page object with QuerySet of all segments
    paginator = Paginator(segmenttype_list, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'replay/segmenttype_list.html', context=context)

def segment_type_detail_slug_view(request, slug):
    """Return a HttpResponse to display list of ReplayEpisodes that are part of a single SegmentType, given slug for specific SegmentType."""
    segmenttype = get_object_or_404(SegmentType, slug=slug)

    # Create base context to display list passing in ReplayEpisodes with 
    # matching SegmentType as the QuerySet.
    context = creat_sort_filter_context_replay(
        request, 
        ReplayEpisode.objects.filter(other_segments__type=segmenttype.id).distinct(), 
    )

    return render(request, 'replay/segmenttype_detail.html', context=context)

# Random ReplayEpisode from AJAX request

def get_random_replay_episode_inst():
    """Return a random instance of ReplayEpisode OR None if no ReplayEpisodes in database."""
    pks = ReplayEpisode.objects.values_list('pk', flat=True)
    
    if pks:
        random_pk = choice(pks)
        return ReplayEpisode.objects.get(pk=random_pk)
    else:
        return None

def get_random_replay_episode(request):
    """Return a HttpResponse from an AJAX request for random Replay episode."""
    if request.method != 'GET':
        return HttpResponse('Request method is NOT a GET')
    
    replayepisode = get_random_replay_episode_inst()

    return HttpResponse(
        render_to_string(
            'replayepisode_basic_tag.html',
            context={
                'episode': replayepisode.show_episode.episode,
                'replayepisode': replayepisode,
            }
        )
    )
