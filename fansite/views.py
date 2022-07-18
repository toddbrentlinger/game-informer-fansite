from django.shortcuts import render
from django.db.models import Q
from games.models import Game, Platform, Developer, Collection, Franchise, Genre, Theme, Keyword
from replay.models import ReplayEpisode, SegmentType
from people.models import Person

# Create your views here.

def index(request):
    '''View function for home page of site.'''

    # Generate counts of some objects
    context = {
        'num_replay_episodes': ReplayEpisode.objects.count(),
        'num_games': Game.objects.count(),
        'num_replay_segment_types': SegmentType.objects.count(),
        'num_game_platforms': Platform.objects.count(),
        'num_game_developers': Developer.objects.count(),
        'num_people': Person.objects.count(),
        'num_game_collections': Collection.objects.count(),
        'num_game_franchises': Franchise.objects.count(),
        'num_game_genres': Genre.objects.count(),
        'num_game_themes': Theme.objects.count(),
        'num_game_keywords': Keyword.objects.count(),
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def search(request):
    '''View function for whole site search.'''

    search_input = request.GET['q']

    context = {
        'replayepisodes': ReplayEpisode.objects.filter(
            Q(title__unaccent__icontains=search_input) 
            | Q(main_segment_games__name__unaccent__icontains=search_input)
            | Q(other_segments__games__name__unaccent__icontains=search_input)
        ).distinct(),
        'games': Game.objects.filter(
            Q(name__unaccent__icontains=search_input)
            | Q(keywords__name__unaccent__icontains=search_input)
            | Q(themes__name__unaccent__icontains=search_input)
        ).distinct(),
        'people': Person.objects.filter(
            Q(full_name__unaccent__icontains=search_input)
            | Q(short_name__unaccent__icontains=search_input)
        ).distinct(),
    }

    return render(request, 'search.html', context=context)