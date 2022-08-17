from django import template

register = template.Library()

@register.inclusion_tag('replayepisode_basic_tag.html')
def replayepisode_basic_display(replayepisode):
    return {'episode': replayepisode}

@register.inclusion_tag('replayepisode_basic_list_tag.html')
def replayepisode_basic_list_display(replayepisode_page_obj):
    return {'episode_page_obj': replayepisode_page_obj}

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