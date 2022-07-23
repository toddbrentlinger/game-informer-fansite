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
def create_page_selection(paginator, curr_page):
    return {
        'paginator': paginator,
        'curr_page': curr_page,
    }

@register.filter
def add_commas_to_num(val):
    if not val and val != 0:
        return '-'
    return f'{val:,}'