from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Game

# Create your views here.

class GameListView(generic.ListView):
    model = Game

class GameDetailView(generic.DetailView):
    model = Game

def game_detail_slug_view(request, stub):
    game = get_object_or_404(Game, slug=stub)
    return render(request, 'games/game_detail.html', context={'game': game})