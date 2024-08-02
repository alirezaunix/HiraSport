# templatetags/custom_filters.py
from django import template

register = template.Library()


@register.filter(name='dict_filter')
def dict_filter(dictionary, key):
    try:
        return dictionary[key]
    except :
        return None  # or you can return a default value
