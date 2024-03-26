from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Episode

def creat_sort_filter_context(request, query_set, sort_prefix = ''):
    """Return a base context object for sorted and filtered Episode list."""
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

    # Sort direction initialized with default 'descending'
    sort_direction = request.GET.get('dir', 'des')

    # TODO: Limit between 0 to max value (100?)
    max_displayed = request.GET.get('display', 25)

    if (sort_direction == 'asc'):
        query_set = query_set.order_by(F(sort_prefix + sort).asc(nulls_last=True))
    else:
        query_set = query_set.order_by(F(sort_prefix + sort).desc(nulls_last=True))

    paginator = Paginator(query_set, max_displayed)
    page_number = request.GET.get('page')
    episode_page_obj = paginator.get_page(page_number)

    return {
        'episode_page_obj': episode_page_obj,
        'sort': {
            'type': sort_type,
            'direction': sort_direction,
        },
    }

def episode_list_view(request):
    """Return a HttpResponse to display list of Episodes that are filtered and sorted depending on request."""
    context = creat_sort_filter_context(request, Episode.objects.all())

    return render(request, 'episodes/episode_list.html', context=context)

class EpisodeDetailView(generic.DetailView):
    """Return a HttpResponse using generic DetailView to display single Episode detail, given primary key for specific Episode.""" 
    model = Episode

def episode_detail_slug_view(request, slug):
    """Return a HttpResponse to display single Episode detail, given slug for specific Episode."""
    episode = get_object_or_404(Episode, slug=slug)

    context = { 'episode': episode, }

    # Use same generic detail view HTML template, passing episode in context
    return render(request, 'episodes/episode_detail.html', context=context)
