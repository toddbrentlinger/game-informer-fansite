from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from games.models import Game, Platform, Developer, Collection, Franchise, Genre, Theme, Keyword
from replay.models import ReplayEpisode, SegmentType
from people.models import Person
from episodes.models import Episode, YouTubeVideo
from superreplay.models import SuperReplay, SuperReplayEpisode
from shows.models import ShowEpisode

from random import choice

# Create your views here.

def index(request):
    '''View function for home page of site.'''

    # Random items
    pks = ReplayEpisode.objects.values_list('pk', flat=True)
    if pks:
        random_pk = choice(pks)
        random_replayepisode = ReplayEpisode.objects.get(pk=random_pk)
    else:
        random_replayepisode = None

    # Generate counts of some objects
    context = {
        'num_episodes': Episode.objects.count(),

        'num_replay_episodes': ReplayEpisode.objects.count(),
        'num_replay_segment_types': SegmentType.objects.count(),

        'num_super_replays': SuperReplay.objects.count(),
        'num_super_replay_episodes': SuperReplayEpisode.objects.count(),

        'num_youtube_videos': YouTubeVideo.objects.count(),

        'num_games': Game.objects.count(),
        'num_game_platforms': Platform.objects.count(),
        'num_game_developers': Developer.objects.count(),
        'num_people': Person.objects.count(),
        'num_game_collections': Collection.objects.count(),
        'num_game_franchises': Franchise.objects.count(),
        'num_game_genres': Genre.objects.count(),
        'num_game_themes': Theme.objects.count(),
        'num_game_keywords': Keyword.objects.count(),

        'random_replayepisode': random_replayepisode,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def search(request):
    '''View function for whole site search.'''

    search_input = request.GET['q']

    replayepisodes = ReplayEpisode.objects.filter(
        Q(show_episode__episode__title__unaccent__icontains=search_input) 
        | Q(main_segment_games__name__unaccent__icontains=search_input)
        | Q(other_segments__games__name__unaccent__icontains=search_input)
    ).distinct()

    games = Game.objects.filter(
        Q(name__unaccent__icontains=search_input)
        | Q(keywords__name__unaccent__icontains=search_input)
        | Q(themes__name__unaccent__icontains=search_input)
    ).distinct()

    people = Person.objects.filter(
        Q(full_name__unaccent__icontains=search_input)
        | Q(short_name__unaccent__icontains=search_input)
    ).distinct()

    replayepisodes_paginator = Paginator(replayepisodes, 20)
    games_paginator = Paginator(games, 20)
    people_paginator = Paginator(people, 20)

    context = {
        #'replayepisodes': replayepisodes,
        #'replayepisodes_paginator': replayepisodes_paginator,
        'replayepisodes_page_obj': replayepisodes_paginator.get_page(1),
        #'games': games,
        'games_paginator': games_paginator,
        'games_page_obj': games_paginator.get_page(1),
        #'people': people,
        'people_paginator': people_paginator,
        'people_page_obj': people_paginator.get_page(1),
    }

    return render(request, 'search.html', context=context)