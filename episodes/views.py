from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Episode

class EpisodeListView(generic.ListView):
    model = Episode
    paginate_by = 20

def episode_list_view(request):
    sort = request.GET.get('sort', 'airdate')
    direction = request.GET.get('dir', 'desc')
    if direction == 'desc':
        sort = '-' + sort
    
    episode_list = Episode.objects.all().order_by(sort)
    paginator = Paginator(episode_list, 20)

    page_number = request.GET.get('page')
    episode_page_obj = paginator.get_page(page_number)

    context = {
        'episode_page_obj': episode_page_obj,
        'sort': sort,
        'direction': direction,
    }

    return render(request, 'episodes/episode_list.html', context=context)

class EpisodeDetailView(generic.DetailView):
    model = Episode

def episode_detail_slug_view(request, slug):
    episode = get_object_or_404(Episode, slug=slug)

    context = {
        'episode': episode,
    }

    return render(request, 'episodes/episode_detail.html', context=context)
