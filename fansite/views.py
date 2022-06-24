from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import ReplayEpisode
from games.models import Game

# Create your views here.

def index(request):
    """View function for home page of site."""

    # Generate counts of some objects
    num_replay_episodes = ReplayEpisode.objects.count()
    num_games = Game.objects.count()

    context = {
        'num_replay_episodes': num_replay_episodes,
        'num_games': num_games,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class ReplayEpisodeListView(generic.ListView):
    model = ReplayEpisode

class ReplayEpisodeDetailView(generic.DetailView):
    model = ReplayEpisode

def replay_episode_detail_view(request, pk):
    replayepisode = get_object_or_404(ReplayEpisode, pk=pk)
    (season_num, season_episode_num) = replayepisode.get_season()
    context = {
        'replayepisode': replayepisode,
        'season_num': season_num,
        'season_episode_num': season_episode_num
    }
    return render(request, 'fansite/replayepisode_detail.html', context=context)