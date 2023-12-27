from django import template

register = template.Library()

@register.filter
def split_string(value, delimiter):
    value = str(value)
    return value.split(delimiter)

# from django.template import Library
# register = Library()

# @register.filter(name='range')
# def filter_range(start, end):
#     return range(start, end)