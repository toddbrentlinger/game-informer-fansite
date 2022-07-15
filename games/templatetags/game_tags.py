from django import template

register = template.Library()

@register.inclusion_tag('game_basic_tag.html')
def game_basic_display(game):
    return {'game': game}