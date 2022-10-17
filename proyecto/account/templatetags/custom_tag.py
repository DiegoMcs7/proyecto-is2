from django import template

register = template.Library()

@register.simple_tag
def add(a):
    a = a+1
    return a