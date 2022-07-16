from django import template

register = template.Library()

@register.inclusion_tag('game_basic_list_tag.html')
def game_basic_list_display(game_list):
    return {'game_list': game_list}