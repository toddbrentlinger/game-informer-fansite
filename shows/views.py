from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Show, ShowEpisode

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

class ShowEpisodeListView(generic.ListView):
    model = ShowEpisode
    paginate_by = 20

class ShowEpisodeDetailView(generic.DetailView):
    model = ShowEpisode

def showepisode_detail_slug_view(request, slug):
    showepisode = get_object_or_404(ShowEpisode, slug=slug)

    context = {
        'showepisode': showepisode,
    }

    return render(request, 'shows/showepisode_detail.html', context=context)
