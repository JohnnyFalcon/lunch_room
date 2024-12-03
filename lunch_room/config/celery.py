# your_project/celery.py
import os
from celery import Celery

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('lunch_room')


app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'check-lunch-sessions': {
        'task': 'lunch_app.tasks.update_expired_sessions',
        'schedule': 60.0,
    }
}


app.autodiscover_tasks()