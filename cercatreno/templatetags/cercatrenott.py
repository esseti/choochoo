__author__ = 'stefanotranquillini'
from django import template

register = template.Library()
@register.filter(name='note_to_class')
def note_to_class(value):
    if "ritardo" in value:
        return 'error'
    elif "in orario" in value:
        return 'success'
    else:
        return 'info'