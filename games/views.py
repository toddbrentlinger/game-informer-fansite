from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Q
from .models import Developer, Game, Genre, Platform, Developer, Collection, Franchise, Theme, Keyword
from replay.models import ReplayEpisode

# Create your views here.

class GameListView(generic.ListView):
    model = Game
    paginate_by = 20

class GameDetailView(generic.DetailView):
    model = Game

def game_detail_slug_view(request, slug):
    game = get_object_or_404(Game, slug=slug)

    replayepisode_list = ReplayEpisode.objects.filter(
        Q(main_segment_games__id=game.id)
        | Q(other_segments__games__id=game.id)
    ).distinct()

    context = {
        'game': game,
        'replayepisode_list': replayepisode_list
    }

    return render(request, 'games/game_detail.html', context=context)

class PlatformListView(generic.ListView):
    model = Platform
    paginate_by = 20

class PlatformDetailView(generic.DetailView):
    model = Platform

def platform_detail_slug_view(request, slug):
    platform = get_object_or_404(Platform, slug=slug)
    return render(request, 'games/platform_detail.html', context={ 
        'object': platform,
        'game_list': platform.game_set.all,
        'model_name': 'platform',
    })
    #return render(request, 'games/platform_detail_old.html', context={'platform': platform})

class DeveloperListView(generic.ListView):
    model = Developer
    paginate_by = 20

class DeveloperDetailView(generic.DetailView):
    model = Developer

def developer_detail_slug_view(request, slug):
    developer = get_object_or_404(Developer, slug=slug)
    return render(request, 'games/developer_detail.html', context={ 
        'object': developer,
        'game_list': developer.game_set.all,
        'model_name': 'developer' 
    })
    #return render(request, 'games/developer_detail.html', context={'developer': developer})

class CollectionListView(generic.ListView):
    model = Collection
    paginate_by = 20

class CollectionDetailView(generic.DetailView):
    model = Collection

def collection_detail_slug_view(request, slug):
    collection = get_object_or_404(Collection, slug=slug)
    return render(request, 'base_game_detail.html', context={ 
        'object': collection,
        'game_list': collection.games.all,
        'model_name': 'collection' 
    })

class FranchiseListView(generic.ListView):
    model = Franchise
    paginate_by = 20

class FranchiseDetailView(generic.DetailView):
    model = Franchise

def franchise_detail_slug_view(request, slug):
    franchise = get_object_or_404(Franchise, slug=slug)
    return render(request, 'base_game_detail.html', context={ 
        'object': franchise,
        'game_list': franchise.games.all,
        'model_name': 'franchise' 
    })

class GenreListView(generic.ListView):
    model = Genre
    paginate_by = 20

class GenreDetailView(generic.DetailView):
    model = Genre

def genre_detail_slug_view(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    return render(request, 'base_game_detail.html', context={ 
        'object': genre,
        'game_list': genre.game_set.all,
        'model_name': 'genre' 
    })

class ThemeListView(generic.ListView):
    model = Theme
    paginate_by = 20

class ThemeDetailView(generic.DetailView):
    model = Theme

def theme_detail_slug_view(request, slug):
    theme = get_object_or_404(Theme, slug=slug)
    return render(request, 'base_game_detail.html', context={ 
        'object': theme,
        'game_list': theme.game_set.all,
        'model_name': 'theme' 
    })

class KeywordListView(generic.ListView):
    model = Keyword
    paginate_by = 20

class KeywordDetailView(generic.DetailView):
    model = Keyword

def keyword_detail_slug_view(request, slug):
    keyword = get_object_or_404(Keyword, slug=slug)
    return render(request, 'base_game_detail.html', context={ 
        'object': keyword,
        'game_list': keyword.game_set.all,
        'model_name': 'keyword' 
    })
