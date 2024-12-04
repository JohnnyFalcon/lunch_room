from django.apps import AppConfig


class LunchRoomConfig(AppConfig):
    name = 'lunch_room'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        from . import signals
        from . import tasks
