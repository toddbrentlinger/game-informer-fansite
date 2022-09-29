from django import template

register = template.Library()

@register.inclusion_tag('replayepisode_basic_tag.html')
def replayepisode_basic_display(replayepisode):
    return {'episode': replayepisode.show_episode.episode}

@register.inclusion_tag('replayepisode_basic_list_tag.html')
def replayepisode_basic_list_display(replayepisode_page_obj):
    return {'episode_page_obj': replayepisode_page_obj}
