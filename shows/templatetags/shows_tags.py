from django import template
from episodes.templatetags.episodes_tags import create_episode_basic_list_display_context

register = template.Library()

@register.inclusion_tag('show_basic_tag.html')
def show_basic_display(show):
    """Tag to display single Show instance data."""
    return {'show': show}

@register.inclusion_tag('show_basic_list_tag.html')
def show_basic_list_display(show_list):
    """Tag to display list of Show instances."""
    return {'show_list': show_list}

@register.inclusion_tag('showepisode_basic_tag.html')
def showepisode_basic_display(showepisode):
    """Tag to display single ShowEpisode instance data."""
    return {
        'episode': showepisode.episode,
        'showepisode': showepisode
    }

@register.inclusion_tag('showepisode_basic_list_tag.html')
def showepisode_basic_list_display(showepisode_page_obj, sort, filter, get_query):
    """Tag to display list of ShowEpisode instances with sort and filter functionality."""
    return create_episode_basic_list_display_context(showepisode_page_obj, sort, filter, get_query)
