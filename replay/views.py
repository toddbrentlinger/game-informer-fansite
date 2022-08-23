from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import ReplayEpisode, Segment, SegmentType

# Create your views here.

class ReplayEpisodeListView(generic.ListView):
    model = ReplayEpisode
    paginate_by = 20

def replay_episode_list_view(request):
    replay_episode_list = ReplayEpisode.objects.all()
    paginator = Paginator(replay_episode_list, 20)

    page_number = request.GET.get('page')
    replay_episode_page_obj = paginator.get_page(page_number)

    context = {
        'episode_page_obj': replay_episode_page_obj,
    }

    return render(request, 'replay/replayepisode_list.html', context=context)

class ReplayEpisodeDetailView(generic.DetailView):
    model = ReplayEpisode

def replay_episode_detail_view(request, pk):
    replayepisode = get_object_or_404(ReplayEpisode, pk=pk)
    context = {
        'episode': replayepisode
    }
    return render(request, 'replay/replayepisode_detail.html', context=context)

def replay_episode_detail_slug_view(request, slug):
    replayepisode = get_object_or_404(ReplayEpisode, slug=slug)
    (season_num, season_episode_num) = replayepisode.get_season()
    context = {
        'episode': replayepisode,
        'season_num': season_num,
        'season_episode_num': season_episode_num
    }
    return render(request, 'replay/replayepisode_detail.html', context=context)

class SegmentTypeListView(generic.ListView):
    model = SegmentType
    paginate_by = 20

def segment_type_list_view(request):
    segmenttype_list = SegmentType.objects.all()
    paginator = Paginator(segmenttype_list, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'replay/segmenttype_list.html', context=context)

class SegmentTypeDetailView(generic.DetailView):
    model = SegmentType

def segment_type_detail_slug_view(request, slug):
    segmenttype = get_object_or_404(SegmentType, slug=slug)

    replayepisode_list = ReplayEpisode.objects.filter(other_segments__type=segmenttype.id).distinct()
    paginator = Paginator(replayepisode_list, 20)

    page_number = request.GET.get('page')
    replayepisode_page_obj = paginator.get_page(page_number)

    context = {
        'segmenttype': segmenttype,
        'episode_page_obj': replayepisode_page_obj,
    }

    # context = {
    #     'segmenttype': segmenttype,
    #     'replayepisode_list': replayepisode_list
    # }
    
    return render(request, 'replay/segmenttype_detail.html', context=context)
