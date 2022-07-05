from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Developer, Game, Platform, Developer

# Create your views here.

class GameListView(generic.ListView):
    model = Game
    paginate_by = 20

class GameDetailView(generic.DetailView):
    model = Game

def game_detail_slug_view(request, stub):
    game = get_object_or_404(Game, slug=stub)
    return render(request, 'games/game_detail.html', context={'game': game})

class PlatformListView(generic.ListView):
    model = Platform
    paginate_by = 20

class PlatformDetailView(generic.DetailView):
    model = Platform

def platform_detail_slug_view(request, stub):
    platform = get_object_or_404(Platform, slug=stub)
    return render(request, 'games/platform_detail.html', context={'platform': platform})

class DeveloperListView(generic.ListView):
    model = Developer
    paginate_by = 20

class DeveloperDetailView(generic.DetailView):
    model = Developer

def developer_detail_slug_view(request, stub):
    developer = get_object_or_404(Developer, slug=stub)
    return render(request, 'games/developer_detail.html', context={'developer': developer})