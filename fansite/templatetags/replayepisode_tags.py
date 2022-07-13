from django import template

register = template.Library()

@register.inclusion_tag('replayepisode_basic_tag.html')
def replayepisode_basic_display(replayepisode):
    return {'replayepisode': replayepisode}