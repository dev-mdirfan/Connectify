from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import markdown


register = template.Library()

@register.filter
def split_string(value, delimiter):
    value = str(value)
    return value.split(delimiter)


@register.filter
@stringfilter
def render_markdown(value):
    md = markdown.Markdown(extensions=["fenced_code"])
    return mark_safe(md.convert(value))


# from django.template import Library
# register = Library()

# @register.filter(name='range')
# def filter_range(start, end):
#     return range(start, end)