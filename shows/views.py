from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Show, Episode

# Create your views here.

class ShowListView(generic.ListView):
    model = Show
    paginate_by = 20

class ShowDetailView(generic.DetailView):
    model = Show

def show_detail_slug_view(request, slug):
    show = get_object_or_404(Show, slug=slug)

    context = {
        'show': show,
    }

    return render(request, 'shows/show_detail.html', context=context)

class EpisodeListView(generic.ListView):
    model = Episode
    paginate_by = 20

class EpisodeDetailView(generic.DetailView):
    model = Episode

def episode_detail_slug_view(request, slug):
    episode = get_object_or_404(Episode, slug=slug)

    context = {
        'episode': episode,
    }

    return render(request, 'shows/episode_detail.html', context=context)
