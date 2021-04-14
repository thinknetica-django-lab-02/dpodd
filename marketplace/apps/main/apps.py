from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'apps.main'

    def ready(self):
        import apps.main.signals
