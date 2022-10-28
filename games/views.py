from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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

class GameCreate(CreateView):
    model = Game
    fields = ['name', 'slug', 'url', 'summary', 'storyline', 'platforms', 'genres', 'keywords', 'themes', 'developers', 'release_date', 'cover', 'websites']

class GameUpdate(UpdateView):
    model = Game
    fields = ['name', 'slug', 'url', 'summary', 'storyline', 'platforms', 'genres', 'keywords', 'themes', 'developers', 'release_date', 'cover', 'websites']

class GameDelete(DeleteView):
    model = Game
    success_url = reverse_lazy('games')

class PlatformListView(generic.ListView):
    model = Platform
    paginate_by = 20

class PlatformDetailView(generic.DetailView):
    model = Platform

def platform_detail_slug_view(request, slug):
    platform = get_object_or_404(Platform, slug=slug)

    paginator = Paginator(platform.game_set.all(), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'games/platform_detail.html', context={ 
        'object': platform,
        'page_obj': page_obj,
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

    paginator = Paginator(developer.game_set.all(), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'games/developer_detail.html', context={ 
        'object': developer,
        'page_obj': page_obj,
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

    paginator = Paginator(collection.games.all(), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'base_game_detail.html', context={ 
        'object': collection,
        'page_obj': page_obj,
        'model_name': 'collection' 
    })

class FranchiseListView(generic.ListView):
    model = Franchise
    paginate_by = 20

class FranchiseDetailView(generic.DetailView):
    model = Franchise

def franchise_detail_slug_view(request, slug):
    franchise = get_object_or_404(Franchise, slug=slug)

    paginator = Paginator(franchise.games.all(), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'base_game_detail.html', context={ 
        'object': franchise,
        'page_obj': page_obj,
        'model_name': 'franchise' 
    })

class GenreListView(generic.ListView):
    model = Genre
    paginate_by = 20

class GenreDetailView(generic.DetailView):
    model = Genre

def genre_detail_slug_view(request, slug):
    genre = get_object_or_404(Genre, slug=slug)

    paginator = Paginator(genre.game_set.all(), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'base_game_detail.html', context={ 
        'object': genre,
        'page_obj': page_obj,
        'model_name': 'genre' 
    })

class ThemeListView(generic.ListView):
    model = Theme
    paginate_by = 20

class ThemeDetailView(generic.DetailView):
    model = Theme

def theme_detail_slug_view(request, slug):
    theme = get_object_or_404(Theme, slug=slug)

    paginator = Paginator(theme.game_set.all(), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'base_game_detail.html', context={ 
        'object': theme,
        'page_obj': page_obj,
        'model_name': 'theme' 
    })

class KeywordListView(generic.ListView):
    model = Keyword
    paginate_by = 20

class KeywordDetailView(generic.DetailView):
    model = Keyword

def keyword_detail_slug_view(request, slug):
    keyword = get_object_or_404(Keyword, slug=slug)

    paginator = Paginator(keyword.game_set.all(), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'base_game_detail.html', context={ 
        'object': keyword,
        'page_obj': page_obj,
        'model_name': 'keyword' 
    })
