from operator import itemgetter
from django import template

register = template.Library()

@register.inclusion_tag('replayepisode_basic_tag.html')
def replayepisode_basic_display(replayepisode):
    return {'replayepisode': replayepisode}

@register.inclusion_tag('heading_tag.html')
def display_heading_json(key, value):
    if key == 'quotes':
        def handle_quotes_map(item):
            if isinstance(item, list):
                return '\n\n'.join(item)
            else:
                return item
        value = map(handle_quotes_map, value)
        value = map(lambda item: item, value)
    return {'key': key, 'value': value}