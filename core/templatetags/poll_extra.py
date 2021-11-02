from django import template
from ..utils import split_timedelta

register = template.Library()

@register.filter(name="br_time")
def format_timedelta_in_pt_br(timedelta):
    
    days, remain_time = split_timedelta(timedelta)
    if days == 0:
        return remain_time
    elif days == 1:
        return "{} dia, {}".format(days, remain_time)
    else:
        return "{} dias, {}".format(days, remain_time)
