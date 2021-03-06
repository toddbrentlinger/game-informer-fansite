from django import template

register = template.Library()

@register.inclusion_tag('replayepisode_basic_tag.html')
def replayepisode_basic_display(replayepisode):
    return {'replayepisode': replayepisode}

@register.inclusion_tag('replayepisode_basic_list_tag.html')
def replayepisode_basic_list_display(replayepisode_list):
    return {'replayepisode_list': replayepisode_list}

@register.inclusion_tag('heading_tag.html')
def display_heading_json(key, value):
    if key == 'quotes':
        def handle_quotes_map(item):
            if isinstance(item, list):
                return '\n\n'.join(item)
            else:
                return item
        value = map(handle_quotes_map, value)
    return {'key': key, 'value': value}