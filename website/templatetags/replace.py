from django import template

register = template.Library()

@register.filter
def blank_remove(value):
    return value.replace(" ","").replace("-","_")