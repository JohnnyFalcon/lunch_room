
from celery import shared_task
from django.utils import timezone
from .models import LunchSession


@shared_task(name='lunch_room.tasks.update_expired_sessions')
def update_expired_sessions():
    """
    Check for expired lunch sessions and update their status.
    This task runs every minute via celery beat as configured in celery.py.

    Returns:
        str: A message indicating how many sessions were updated
    """
    current_time = timezone.now()

    # Get all active sessions that have passed their end time
    expired_sessions = LunchSession.objects.filter(
        status=LunchSession.ACTIVE,
        session_end_time__lt=current_time
    )

    # Update their status to closed
    updated_count = expired_sessions.update(status=LunchSession.CLOSED)

    return f"Updated {updated_count} expired sessions"