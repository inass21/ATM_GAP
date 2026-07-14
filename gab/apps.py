from django.apps import AppConfig


class GabConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gab'

    def ready(self):
        self._patch_datetime_converter()

    @staticmethod
    def _patch_datetime_converter():
        # Certaines lignes de la base contiennent des dates invalides
        # (ex. '0000-00-00 00:00:00') que le pilote renvoie en texte brut,
        # ce qui fait planter make_aware(). On neutralise ces valeurs en None
        # (affichées « — ») sans toucher aux modèles.
        from django.conf import settings
        from django.db.backends.mysql.operations import DatabaseOperations
        from django.utils import timezone

        original = DatabaseOperations.convert_datetimefield_value

        def safe_convert(self, value, expression, connection):
            if isinstance(value, str):
                if not value.strip() or value.startswith("0000-00-00"):
                    return None
                try:
                    from django.utils.dateparse import parse_datetime, parse_date
                    from datetime import datetime, time as dtime

                    parsed = parse_datetime(value)
                    if parsed is None:
                        parsed_date = parse_date(value)
                        parsed = (
                            datetime.combine(parsed_date, dtime.min)
                            if parsed_date
                            else None
                        )
                    if parsed is None:
                        return None
                    if settings.USE_TZ:
                        parsed = timezone.make_aware(
                            parsed, connection.timezone
                        )
                    return parsed
                except Exception:
                    return None
            return original(self, value, expression, connection)

        DatabaseOperations.convert_datetimefield_value = safe_convert
