from django.apps import AppConfig


class DocumentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'local_apps.document'

    def ready(self):
        import local_apps.document.signals
