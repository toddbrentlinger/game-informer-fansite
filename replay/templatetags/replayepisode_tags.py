from django import template
from episodes.templatetags.episodes_tags import create_episode_basic_list_display_context

register = template.Library()

@register.inclusion_tag('replayepisode_basic_tag.html')
def replayepisode_basic_display(replayepisode):
    """Tag to display single Replay episode data."""
    return {
        'episode': replayepisode.show_episode.episode,
        'replayepisode': replayepisode
    }

@register.inclusion_tag('replayepisode_basic_list_tag.html')
def replayepisode_basic_list_display(replayepisode_page_obj, sort, filter, get_query):
    """Tag to display list of Replay episodes with sort and filter functionality."""
    context = create_episode_basic_list_display_context(replayepisode_page_obj, sort, filter, get_query)
    
    # Add sort option that sorts by Replay episode number
    context['sort_options_dict']['replay'] = 'Episode Number'
    
    return context
