# custom_filters.py

from django import template
from datetime import datetime, timedelta
from django.utils import timezone


register = template.Library()

@register.filter(name='format_article_date')
def format_article_date(timestamp):
    current_time = timezone.now()
    today = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - timedelta(days=1)
    seconds_in_hour = timedelta(seconds=60*60)
    seconds_in_minute = timedelta(seconds=60)
    time_diff = current_time - timestamp
    
    if time_diff < seconds_in_minute:
        return f"Just now"
    elif time_diff < seconds_in_hour:
        minutes_ago = int(time_diff.seconds // 60)
        return f"{minutes_ago} minute{'s' if minutes_ago != 1 else ''} ago"
    elif timestamp >= today:
        formatted_time = timestamp.strftime("%I:%M %p")
        return formatted_time
    elif timestamp >= yesterday:
        formatted_time = timestamp.strftime("%I:%M %p")
        return f"Yesterday {formatted_time}"
    else:
        return timestamp.strftime("%b %d, %Y %I:%M %p")
    

@register.filter(name="remove_attr")
def remove_attr(field, attr):
    if attr in field.field.widget.attrs:
        del field.field.widget.attrs[attr]
    return field