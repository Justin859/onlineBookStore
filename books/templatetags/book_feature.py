from django import template
from django.utils.safestring import mark_safe
import markdown2

register = template.Library()

@register.filter(name='img_src')
def img_src(value):
    value = str(value)
    value = value.split("/")[1:]
    return '/'.join(value)

@register.filter('markdown_to_html')
def markdown_to_html(markdown_text):
    '''Converts markdown text to HTML '''   
    html_body = markdown2.markdown(markdown_text)
    return mark_safe(html_body)    

@register.filter('range')
def stars_range(value):
    value = int(float(value))
    return range(1, value+1)

@register.filter('stars_off')
def stars_off(value):
    value = 5 - int(float(value))
    return range(1, value+1)

@register.filter('cut_array')
def cut_array(value, arg):
    arg = arg.split(',')
    value = value[int(arg[1]):int(arg[0])]
    return value

@register.filter('shortner')
def shortner(value):
    value = value.split(" ")
    value = value[:25]
    value = " ".join(value)
    return value