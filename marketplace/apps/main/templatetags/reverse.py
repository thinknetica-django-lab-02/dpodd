from django import template
from django.utils.safestring import SafeString

register = template.Library()


@register.filter
def reverse(value, arg=None):
    print(type(value))
    if not isinstance(value, SafeString):
        return "Error! A string should be provided"
    return value[::-1]
