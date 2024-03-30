from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Show, ShowEpisode
from episodes.models import Episode
from episodes.views import creat_sort_filter_context

class ShowListView(generic.ListView):
    """Return a HttpResponse using generic ListView to display list of Shows."""
    model = Show

def show_detail_slug_view(request, slug):
    """Return a HttpResponse to display list of Episodes that are part of a single Show, given slug for specific Show."""
    # If no slug is provided OR show title slug is 'other', get all Episodes that are NOT part of any show
    if slug is None or slug == 'other':
        # Get QuerySet of all Episodes NOT associated with any ShowEpisode instance
        query_set = Episode.objects.exclude(id__in=ShowEpisode.objects.all().values_list('episode_id', flat=True))
        
        # Create base context to display Episode list with sort and filter options
        context = creat_sort_filter_context(request, query_set)

        # Render using template for no existing Show
        return render(request, 'shows/no_show_detail.html', context=context)
    # Else get all Episodes part of show title slug
    else:
        # Find Show matching slug OR throw 404 Error if NO match found
        show = get_object_or_404(Show, slug=slug)
        
        # Get QuerySet of all ShowEpisodes associated with the Show
        query_set = show.showepisode_set.all()
        
        # Create base context to display Episode list with sort and filter options
        # passing in sort prefix to sort by Episode data instead of ShowEpisode that
        # is passed in QuerySet.
        context = creat_sort_filter_context(request, query_set, 'episode__')
        
        # Add show to context to be used in template
        context['show'] = show
        
        # Render using template for existing Show
        return render(request, 'shows/show_detail.html', context=context)

def showepisode_detail_slug_view(request, *args, **kwargs):
    """Return a HttpResponse to display single ShowEpisode detail, given slugs for specific Show and ShowEpisode."""
    # Show slug
    show = get_object_or_404(Show, slug=kwargs['show_slug'])
    
    # ShowEpisode slug
    showepisode = get_object_or_404(ShowEpisode, show=show, slug=kwargs['showepisode_slug'])

    # Add Episode of ShowEpisode to context that is passed to template
    context = { 'episode': showepisode.episode, }

    return render(request, 'shows/showepisode_detail.html', context=context)
