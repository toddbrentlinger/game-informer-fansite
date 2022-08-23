from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import SuperReplay, SuperReplayEpisode

# Super Replay

def superreplay_list_view(request):
    superreplay_list = SuperReplay.objects.all()
    paginator = Paginator(superreplay_list, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'superreplay_page_obj': page_obj,
    }

    return render(request, 'superreplay/superreplay_list.html', context=context)

class SuperReplayDetailView(generic.DetailView):
    model = SuperReplay

def super_replay_detail_view(request, pk):
    superreplay = get_object_or_404(SuperReplay, pk=pk)

    superreplayepisode_list = superreplay.superreplayepisode_set.all()
    paginator = Paginator(superreplayepisode_list, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'superreplay': superreplay,
        'superreplayepisode_page_obj': page_obj,
    }
    return render(request, 'superreplay/superreplay_detail.html', context=context)

def super_replay_detail_slug_view(request, slug):
    superreplay = get_object_or_404(SuperReplay, slug=slug)
    
    superreplayepisode_list = superreplay.superreplayepisode_set.all()
    paginator = Paginator(superreplayepisode_list, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'superreplay': superreplay,
        'superreplayepisode_page_obj': page_obj,
    }

    return render(request, 'superreplay/superreplay_detail.html', context=context)

# Super Replay Episode

class SuperReplayEpisodeDetailView(generic.DetailView):
    model = SuperReplayEpisode

def super_replay_episode_detail_slug_view(request, slug, num):
    superreplayepisode = get_object_or_404(SuperReplayEpisode, super_replay__slug=slug, episode_number=num)
    context = {
        'episode': superreplayepisode,
    }
    return render(request, 'superreplay/superreplayepisode_detail.html', context=context)