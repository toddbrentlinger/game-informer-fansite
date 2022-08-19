from django import template

register = template.Library()

@register.inclusion_tag('episode_basic_tag.html')
def episode_basic_display(episode):
    return {'episode': episode}

@register.inclusion_tag('episode_basic_list_tag.html')
def episode_basic_list_display(episode_page_obj):
    return {
        'episode_page_obj': episode_page_obj
    }
