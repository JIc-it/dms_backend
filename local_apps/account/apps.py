from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'local_apps.account'

    def ready(self):
        import local_apps.account.signals
