from django.core.exceptions import FieldError
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Episode

class EpisodeListView(generic.ListView):
    model = Episode
    paginate_by = 20

def episode_list_view(request):
    sort = request.GET.get('sort', '-airdate')
    
    episode_list = Episode.objects.all().order_by(sort)
    paginator = Paginator(episode_list, 20)

    page_number = request.GET.get('page')
    episode_page_obj = paginator.get_page(page_number)

    context = {
        'episode_page_obj': episode_page_obj,
        'sort': sort,
    }

    return render(request, 'episodes/episode_list.html', context=context)

def episode_list_view_ajax(request):
    # Conversions from select option value to query string used in order_by() method
    SORT_TYPES = {
        'likes': 'youtube_video__likes',
        'video-length': 'youtube_video__duration',
        'views': 'youtube_video__views',
    }

    # Sort type initialized with optional '-' prefix
    sort_type = request.GET.get('sort', '-airdate')

    # Sort direction using '-' prefix in sort_type
    ascending = sort_type.startswith('-')
    # If ascending is True, remove '-' prefix from sort_type
    if ascending:
        sort_type = sort_type.removeprefix('-')

    # TODO: Confirm sort type validity. If not, set to 'airdate' OR raise error
    # Could use Form object instead Or try-catch if sort type NOT valid
    
    # Set sort string used in order_by method.
    # Convert select option value if necessary.
    if sort_type in SORT_TYPES.keys():
        sort = SORT_TYPES[sort_type]
    else:
        sort = sort_type

    # Add '-' prefix to sort string if ascending is true
    if ascending:
        sort = '-' + sort_type

    max_displayed = request.GET.get('display', 25)
    # TODO: Limit between 0 to max value (100?)
    
    episode_list = Episode.objects.all().order_by(sort)

    paginator = Paginator(episode_list, max_displayed)

    page_number = request.GET.get('page')
    episode_page_obj = paginator.get_page(page_number)

    context = {
        'episode_page_obj': episode_page_obj,
        'sort_type': sort_type,
        'ascending': ascending,
        'max_displayed': max_displayed,
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
