from django.shortcuts import render
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