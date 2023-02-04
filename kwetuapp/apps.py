from django.apps import AppConfig


class KwetuappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kwetuapp'

    def ready(self):
        import kwetuapp.signals
