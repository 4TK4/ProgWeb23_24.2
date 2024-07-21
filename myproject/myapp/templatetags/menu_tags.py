# myapp/templatetags/menu_tags.py
from django import template

register = template.Library()

@register.simple_tag
def is_active(request, url_name):
    if request.path == url_name:
        return 'active'
    return ''
