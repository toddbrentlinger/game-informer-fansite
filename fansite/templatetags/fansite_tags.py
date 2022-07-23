import math

from django import template

register = template.Library()

@register.inclusion_tag('img_gallery_slider_tag.html')
def create_img_gallery_slider(img_list, src_base, file_type = 'png', alt_append = ''):
    return {
        'item_list': img_list,
        'img_type_name': img_list[0].__class__.__name__ if img_list else 'Image',
        'src_base': src_base,
        'file_type': file_type,
        'alt_append': alt_append,
    }

@register.inclusion_tag('video_gallery_slider_tag.html')
def create_video_gallery_slider(gamevideo_list):
    return {
        'item_list': gamevideo_list,
    }

@register.inclusion_tag('page_selection_tag.html')
def create_page_selection(page_obj, num_page_btns = 5):
    curr_page = page_obj.number
    last_page = page_obj.paginator.num_pages
    middle_page = math.ceil(num_page_btns / 2)

    prev = curr_page == 1
    next = curr_page == last_page
    first = last_page <= num_page_btns or curr_page <= middle_page
    last = last_page <= num_page_btns or curr_page >= last_page - middle_page + 1

    if last_page > num_page_btns:
        if curr_page > last_page - middle_page:
            start = last_page - num_page_btns + 1
            end = last_page
        elif curr_page > middle_page:
            start = curr_page - middle_page + 1
            end = curr_page + middle_page - 1
        else:
            start = 1
            end = num_page_btns
    else:
        start = 1
        end = last_page

    return {
        'page_obj': page_obj,
        'num_page_btns': num_page_btns,
        'prev': prev,
        'next': next,
        'first': first,
        'last': last,
        'range': range(start, end + 1),
    }

@register.filter
def add_commas_to_num(val):
    if not val and val != 0:
        return '-'
    return f'{val:,}'
