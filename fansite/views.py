from django.shortcuts import render
from games.models import Game, Platform, Developer
from replay.models import ReplayEpisode, SegmentType
from people.models import Person

# Create your views here.

def index(request):
    """View function for home page of site."""

    # Generate counts of some objects
    context = {
        'num_replay_episodes': ReplayEpisode.objects.count(),
        'num_games': Game.objects.count(),
        'num_replay_segment_types': SegmentType.objects.count(),
        'num_game_platforms': Platform.objects.count(),
        'num_game_developers': Developer.objects.count(),
        'num_people': Person.objects.count()
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)