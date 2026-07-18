from django.apps import AppConfig


class StatistiquesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'statistiques'

    def ready(self):
        # Branche les signaux d'invalidation du cache des statistiques.
        from . import signals  # noqa: F401
