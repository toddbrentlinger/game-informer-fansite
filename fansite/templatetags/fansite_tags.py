from django import template

register = template.Library()

@register.filter
def add_commas_to_num(val):
    if not val and val != 0:
        return '-'
    return f'{val:,}'