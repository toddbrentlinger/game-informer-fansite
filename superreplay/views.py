from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import SuperReplay, SuperReplayEpisode

# Create your views here.

class SuperReplayListView(generic.ListView):
    model = SuperReplay
    paginate_by = 20

class SuperReplayDetailView(generic.DetailView):
    model = SuperReplay

def super_replay_detail_view(request, pk):
    superreplay = get_object_or_404(SuperReplay, pk=pk)
    context = {
        'superreplay': superreplay
    }
    return render(request, 'super-replay/superreplay_detail.html', context=context)

def super_replay_detail_slug_view(request, slug):
    superreplay = get_object_or_404(SuperReplay, slug=slug)
    context = {
        'superreplay': superreplay,
    }
    return render(request, 'super-replay/superreplay_detail.html', context=context)