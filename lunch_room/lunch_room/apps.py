from django.apps import AppConfig


class LunchRoomConfig(AppConfig):
    name = 'lunch_room'

    def ready(self):
        from . import signals
