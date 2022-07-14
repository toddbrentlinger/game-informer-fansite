from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import ReplayEpisode, SegmentType

# Create your views here.

class ReplayEpisodeListView(generic.ListView):
    model = ReplayEpisode
    paginate_by = 20

class ReplayEpisodeDetailView(generic.DetailView):
    model = ReplayEpisode

def replay_episode_detail_view(request, pk):
    replayepisode = get_object_or_404(ReplayEpisode, pk=pk)
    context = {
        'replayepisode': replayepisode
    }
    return render(request, 'replay/replayepisode_detail.html', context=context)

def replay_episode_detail_slug_view(request, stub):
    replayepisode = get_object_or_404(ReplayEpisode, slug=stub)
    (season_num, season_episode_num) = replayepisode.get_season()
    context = {
        'replayepisode': replayepisode,
        'season_num': season_num,
        'season_episode_num': season_episode_num
    }
    return render(request, 'replay/replayepisode_detail.html', context=context)

class SegmentTypeListView(generic.ListView):
    model = SegmentType
    paginate_by = 20

class SegmentTypeDetailView(generic.DetailView):
    model = SegmentType

def segment_type_detail_slug_view(request, stub):
    segmenttype = get_object_or_404(SegmentType, slug=stub)
    return render(request, 'replay/segmenttype_detail.html', context={'segmenttype': segmenttype})
