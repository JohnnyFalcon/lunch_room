from datetime import timedelta

from django import template
from django.utils import timezone

register = template.Library()



@register.inclusion_tag('lunch_room/pages/single_lunch_session.html', takes_context=True)
def render_single_session(context, lunch_session):
    now = timezone.now()

    time_left = lunch_session.session_end_time - now if lunch_session.session_end_time else None
    formatted_time = None

    if time_left:
        if time_left < timedelta():
            formatted_time = "Sesja zakończona"
        else:
            minutes = int(time_left.total_seconds() / 60)
            formatted_time = f"{minutes} minut" if minutes > 0 else "< 1 minuty"

    is_active = lunch_session.status == lunch_session.ACTIVE

    return {
        'lunch_session': lunch_session,
        'permissions': context.get('permissions', {}),
        'time_remaining': formatted_time,
        'is_active': is_active
    }


@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key)) or dictionary.get(int(key), 0)