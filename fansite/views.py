from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from games.models import Game, Platform, Developer, Collection, Franchise, Genre, Theme, Keyword
from replay.models import ReplayEpisode, SegmentType
from replay.views import get_random_replay_episode_inst
from people.models import Person
from episodes.models import Episode, YouTubeVideo
from superreplay.models import SuperReplay, SuperReplayEpisode
from shows.models import ShowEpisode

# Create your views here.

def index(request):
    '''View function for home page of site.'''

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

        'random_replayepisode': get_random_replay_episode_inst(),
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

def get_episodes(request):
    if request.method == 'GET':
        sort = request.GET.get('sort', '-airdate')
        episode_list = Episode.objects.all().order_by(sort)
        paginator = Paginator(episode_list, 20)
        page_number = request.GET.get('page')
        episode_page_obj = paginator.get_page(page_number)

        response = HttpResponse(
            render_to_string(
                'episode_basic_list_tag.html',
                context={
                    'episode_page_obj': episode_page_obj,
                }
            )
        )
        
        return response
    else:
        return HttpResponse('Request method is NOT a GET')
