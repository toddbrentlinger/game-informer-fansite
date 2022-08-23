from django import template

register = template.Library()

@register.inclusion_tag('superreplay_basic_tag.html')
def superreplay_basic_display(superreplay):
    return {'superreplay': superreplay}

@register.inclusion_tag('superreplay_basic_list_tag.html')
def superreplay_basic_list_display(superreplay_page_obj):
    return {'superreplay_page_obj': superreplay_page_obj}

@register.inclusion_tag('superreplayepisode_basic_tag.html')
def superreplayepisode_basic_display(superreplayepisode):
    return {'episode': superreplayepisode}

@register.inclusion_tag('superreplayepisode_basic_list_tag.html')
def superreplayepisode_basic_list_display(superreplayepisode_page_obj):
    return {'episode_page_obj': superreplayepisode_page_obj}