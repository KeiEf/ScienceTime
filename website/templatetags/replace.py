from django import template

register = template.Library()

@register.filter
def blank_remove(value):
    return value.replace(" ","").replace("-","_")

@register.filter
def math_scroll(value):
    return value.replace("\\begin{align}","<div class='eq'>\n\\begin{align}").replace("\\end{align}","\\end{align}</div>").replace("\\begin{equation}","<div class='eq'>\n\\begin{equation}").replace("\\end{equation}","\\end{equation}</div>")