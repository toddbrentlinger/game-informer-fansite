from django import template

register = template.Library()

@register.inclusion_tag('superreplay_basic_tag.html')
def superreplay_basic_display(superreplay):
    return {'superreplay': superreplay}

@register.inclusion_tag('superreplay_basic_list_tag.html')
def superreplay_basic_list_display(superreplay_list):
    return {'superreplay_list': superreplay_list}
