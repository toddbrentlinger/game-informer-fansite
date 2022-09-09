from django import template

register = template.Library()

@register.inclusion_tag('show_basic_tag.html')
def show_basic_display(show):
    return {'show': show}

@register.inclusion_tag('show_basic_list_tag.html')
def show_basic_list_display(show_list):
    return {'show_list': show_list}

@register.inclusion_tag('showepisode_basic_tag.html')
def showepisode_basic_display(showepisode):
    return {
        'episode': showepisode.episode,
        'showepisode': showepisode
    }

@register.inclusion_tag('showepisode_basic_list_tag.html')
def showepisode_basic_list_display(showepisode_page_obj):
    return {'episode_page_obj': showepisode_page_obj}
