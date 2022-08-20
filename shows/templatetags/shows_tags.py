from django import template

register = template.Library()

@register.inclusion_tag('show_basic_tag.html')
def show_basic_display(show):
    return {'show': show}

@register.inclusion_tag('show_basic_list_tag.html')
def show_basic_list_display(show_list):
    return {'show_list': show_list}
