from django import template

register = template.Library()

@register.inclusion_tag('game_basic_list_tag.html')
def game_basic_list_display(page_obj, get_query):
    return {
        'page_obj': page_obj,
        'get_query': get_query
    }