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

    # Sort type initialized with default 'airdate'
    sort_type = request.GET.get('sort', 'airdate')
    
    # TODO: Confirm sort type validity. If not, set to 'airdate' OR raise error
    # Could use Form object instead Or try-catch if sort type NOT valid
    
    # Set sort string used in order_by method.
    # Convert select option value if necessary.
    if sort_type in SORT_TYPES.keys():
        sort = SORT_TYPES[sort_type]
    else:
        sort = sort_type

    # Sort direction initialized with default 'ascending'
    sort_direction = request.GET.get('dir', 'asc')

    # Add '-' prefix to sort string if descending is True
    if sort_direction == 'desc':
        sort = '-' + sort

    max_displayed = request.GET.get('display', 25)
    # TODO: Limit between 0 to max value (100?)
    
    episode_list = Episode.objects.all().order_by(sort)

    paginator = Paginator(episode_list, max_displayed)

    page_number = request.GET.get('page')
    episode_page_obj = paginator.get_page(page_number)

    context = {
        'episode_page_obj': episode_page_obj,
        'sort': {
            'type': sort_type,
            'direction': sort_direction,
        },
        'max_displayed': max_displayed,
        'get_query': request.GET.copy(),
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
