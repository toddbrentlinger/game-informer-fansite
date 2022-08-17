from django.core.paginator import Paginator
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

    show_episodes_list = show.episode_set.all()
    paginator = Paginator(show_episodes_list, 20)

    page_number = request.GET.get('page')
    episode_page_obj = paginator.get_page(page_number)

    context = {
        'show': show,
        'episode_page_obj': episode_page_obj,
    }

    return render(request, 'shows/show_detail.html', context=context)

class EpisodeListView(generic.ListView):
    model = Episode
    paginate_by = 20

def episode_list_view(request):
    episode_list = Episode.objects.all()
    paginator = Paginator(episode_list, 20)

    page_number = request.GET.get('page')
    episode_page_obj = paginator.get_page(page_number)

    context = {
        'episode_page_obj': episode_page_obj,
    }

    return render(request, 'shows/episode_list.html', context=context)

class EpisodeDetailView(generic.DetailView):
    model = Episode

def episode_detail_slug_view(request, slug):
    episode = get_object_or_404(Episode, slug=slug)

    context = {
        'episode': episode,
    }

    return render(request, 'shows/episode_detail.html', context=context)
