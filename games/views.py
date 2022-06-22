from django.shortcuts import render
from django.views import generic
from .models import Game

# Create your views here.

class GameListView(generic.ListView):
    model = Game

class GameDetailView(generic.DetailView):
    model = Game