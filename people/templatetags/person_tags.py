from django import template

register = template.Library()

@register.inclusion_tag('person_basic_tag.html')
def person_basic_display(person):
    return {'person': person}

@register.inclusion_tag('person_basic_list_tag.html')
def person_basic_list_display(page_obj):
    return {'page_obj': page_obj}