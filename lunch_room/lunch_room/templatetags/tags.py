import datetime
from django import template

register = template.Library()


@register.inclusion_tag('lunch_room/pages/single_lunch_session.html', takes_context=True)
def render_single_session(context, lunch_session):
    now = datetime.datetime.now()
    session_end = lunch_session.session_end_time

    time_diff_seconds = int(session_end.timestamp() - now.timestamp())
    minutes = int(time_diff_seconds / 60)

    if minutes < 0:
        formatted_time = "Sesja zakończona"
    else:
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