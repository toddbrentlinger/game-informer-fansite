from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Show, ShowEpisode
from episodes.models import Episode

class ShowListView(generic.ListView):
    model = Show
    paginate_by = 20

class ShowDetailView(generic.DetailView):
    model = Show

def show_detail_slug_view(request, slug):
    if slug is None or slug == 'other':
        show = None
        show_episodes_list = Episode.objects.filter(shows__isnull=True)
    else:
        show = get_object_or_404(Show, slug=slug)
        show_episodes_list = show.showepisode_set.all()

    paginator = Paginator(show_episodes_list, 20)
    page_number = request.GET.get('page')
    episode_page_obj = paginator.get_page(page_number)

    context = {
        'show': show,
        'episode_page_obj': episode_page_obj,
    }

    return render(request, 'shows/show_detail.html', context=context)

def showepisode_detail_slug_view(request, *args, **kwargs):
    # show_slug
    #show = get_object_or_404(Show, slug=kwargs['show_slug'])
    show = Show.objects.get(slug=kwargs['show_slug'])
    
    # showepisode_slug
    #showepisode = get_object_or_404(show=show, slug=kwargs['showepisode_slug'])
    showepisode = ShowEpisode.objects.get(show=show, slug=kwargs['showepisode_slug'])

    context = {
        'showepisode': showepisode,
    }

    return render(request, 'shows/showepisode_detail.html', context=context)
