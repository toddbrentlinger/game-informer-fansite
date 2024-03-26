from django import template

register = template.Library()

def create_episode_basic_list_display_context(episode_page_obj, sort, filter, get_query):
    """Return base context for tag that displays list of episodes with sort and filter functionality."""
    max_displayed_options = [10, 25, 50, 100, 200,]
    
    # Add new max displayed option if NOT in list
    if episode_page_obj.paginator.per_page not in max_displayed_options:
        for i, num in enumerate(max_displayed_options):
            if episode_page_obj.paginator.per_page < num:
                max_displayed_options.insert(
                    i, 
                    episode_page_obj.paginator.per_page
                )
                break

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
        'max_displayed_options': max_displayed_options,
        'get_query': get_query,
    }

@register.inclusion_tag('episode_basic_tag.html')
def episode_basic_display(episode):
    """Tag to display single episode data."""
    return {'episode': episode}

@register.inclusion_tag('episode_basic_list_tag.html')
def episode_basic_list_display(episode_page_obj, sort, filter, get_query):
    """Tag to display list of episodes with sort and filter functionality."""
    return create_episode_basic_list_display_context(episode_page_obj, sort, filter, get_query)

@register.inclusion_tag('heading_tag.html')
def display_heading_json(key, value):
    """Tag to display different heading types for episode heading field."""
    if key == 'quotes':
        def handle_quotes_map(item):
            if isinstance(item, list):
                return '\n\n'.join(item)
            else:
                return item
        value = map(handle_quotes_map, value)
    return {'key': key, 'value': value}