from django import template

register = template.Library()

@register.filter(name="br_time")
def format_timedelta_in_pt_br(timedelta):

    seconds = timedelta.total_seconds()
    days = int(seconds // (60 * 60 * 24))

    seconds = seconds % (60 * 60 * 24)
    hours = int(seconds // (60 * 60))

    seconds = seconds % (60 * 60)
    minutes = int(seconds // 60)

    seconds = int(seconds % 60)

    hours_str = "0{}".format(hours)[-2:]
    minutes_str = "0{}".format(minutes)[-2:]
    seconds_str = "0{}".format(minutes)[-2:]
    if days == 0:
        return "{}:{}:{}".format(hours_str, minutes_str, seconds_str)
    elif days == 1:
        return "{} dia, {}:{}:{}".format(days, hours_str, minutes_str, seconds_str)
    else:
        return "{} dias, {}:{}:{}".format(days, hours_str, minutes_str, seconds_str)
