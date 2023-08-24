from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'local_apps.main'

    def ready(self):
        import local_apps.main.signals
