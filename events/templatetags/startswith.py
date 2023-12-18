from django import template
from datetime import datetime
from django.db.models import Q

register = template.Library()


@register.filter('startswith')
def startswithCust(text, starts):
    return text.startswith(starts)

@register.filter('endswith')
def endswithCust(text, end):
    return text.endswith(str(end))

@register.filter('str_to_date')
def str_to_date(text):
    return datetime.strptime(text, "%Y-%m-%d")

@register.filter('count_for_arr')
def count_for_arr(arr, filterAttr):
    return len(arr.filter(eval(filterAttr)))