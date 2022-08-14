from django import template

register = template.Library()

@register.inclusion_tag('superreplay_basic_tag.html')
def superreplay_basic_display(superreplay):
    return {'superreplay': superreplay}

@register.inclusion_tag('superreplay_basic_list_tag.html')
def superreplay_basic_list_display(superreplay_list):
    return {'superreplay_list': superreplay_list}

@register.inclusion_tag('superreplayepisode_basic_tag.html')
def superreplayepisode_basic_display(superreplayepisode):
    return {'superreplayepisode': superreplayepisode}

@register.inclusion_tag('superreplayepisode_basic_list_tag.html')
def superreplayepisode_basic_list_display(superreplayepisode_list):
    return {'superreplayepisode_list': superreplayepisode_list}