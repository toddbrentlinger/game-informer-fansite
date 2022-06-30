from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import ReplayEpisode, SegmentType, Person
from games.models import Game, Platform, Developer

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

def replay_episode_detail_slug_view(request, stub):
    replayepisode = get_object_or_404(ReplayEpisode, slug=stub)
    (season_num, season_episode_num) = replayepisode.get_season()
    context = {
        'replayepisode': replayepisode,
        'season_num': season_num,
        'season_episode_num': season_episode_num
    }
    return render(request, 'fansite/replayepisode_detail.html', context=context)

class SegmentTypeListView(generic.ListView):
    model = SegmentType

class SegmentTypeDetailView(generic.DetailView):
    model = SegmentType

def segment_type_detail_slug_view(request, stub):
    segmenttype = get_object_or_404(SegmentType, slug=stub)
    return render(request, 'fansite/segmenttype_detail.html', context={'segmenttype': segmenttype})

class PersonListView(generic.ListView):
    model = Person

class PersonDetailView(generic.DetailView):
    model = Person

def person_detail_slug_view(request, stub):
    person = get_object_or_404(Person, slug=stub)
    return render(request, 'fansite/person_detail.html', context={'person': person})