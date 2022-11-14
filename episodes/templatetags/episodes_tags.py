from django import template

register = template.Library()

@register.inclusion_tag('episode_basic_tag.html')
def episode_basic_display(episode):
    return {'episode': episode}

@register.inclusion_tag('episode_basic_list_tag.html')
def episode_basic_list_display(episode_page_obj):
    return {
        'episode_page_obj': episode_page_obj,
    }

@register.inclusion_tag('episode_basic_list_tag.html')
def episode_basic_list_display_ajax(episode_page_obj, sort, filter, get_query):
    return {
        'episode_page_obj': episode_page_obj,
        'sort': sort,
        'sort_options_dict': {
            'airdate': 'Airdate',
            'views': 'Views',
            'likes': 'Likes',
            'video-length': 'Video Length', 
        },
        'filter': filter,
        'max_displayed_options': [10, 25, 50, 100, 200,],
        'get_query': get_query,
    }

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