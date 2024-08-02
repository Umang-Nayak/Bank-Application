from django.apps import AppConfig


class AccountOfficeEngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account_office_engine'

    def ready(self):
        import account_office_engine.signals
