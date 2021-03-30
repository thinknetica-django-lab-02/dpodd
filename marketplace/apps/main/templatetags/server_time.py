import datetime
from django import template

register = template.Library()


@register.simple_tag
def server_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
