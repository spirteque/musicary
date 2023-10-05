from django.template import Library
from django.utils import timesince

register = Library()

#custom template filter - place this in your custom template tags file
@register.filter
def timesince_custom(value):
   #TODO
    return timesince.timesince(value)