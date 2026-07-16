from django.db.models import Count, CharField
from django.db.models.expressions import Func

from gab.models_source import (
    NewIncidentGab,
    NewInteventionIncident,
)

from .filter_service import FilterService


class MonthKey(Func):
    """Clé mois 'YYYY-MM' sans CONVERT_TZ.

    Sous MySQL + USE_TZ=True, TruncMonth génère CONVERT_TZ(...) qui échoue
    quand les tables de timezones MySQL ne sont pas chargées. DATE_FORMAT
    natif évite toute conversion de timezone tout en restant correct (la
    session Django est en UTC, comme TruncMonth).

    Le format '%Y-%m' est transmis comme paramètre lié : MySQLdb ne
    réanalyse jamais les paramètres liés pour '%', ce qui évite l'erreur
    "not enough arguments for format string" / "unsupported format
    character" provoquée par le '%Y' littéral dans le SQL.
    """

    function = "DATE_FORMAT"
    output_field = CharField()

    def as_sql(self, compiler, connection, function=None, template=None):
        # On construit le SQL nous-mêmes pour éviter que Django n'applique
        # son propre formatage '%' (qui entre en conflit avec le '%Y' de
        # DATE_FORMAT et avec la seconde passe de formatage de MySQLdb).
        expression_sql, params = self.source_expressions[0].as_sql(
            compiler, connection
        )
        return "DATE_FORMAT(%s, %%s)" % expression_sql, tuple(params) + ("%Y-%m",)


class EvolutionService:

    @staticmethod
    def get_evolution(filters=None):

        incidents_month = list(
            FilterService.get_incidents_queryset(filters)
            .annotate(month=MonthKey("date_arrete"))
            .values("month")
            .annotate(total=Count("id_incident"))
            .order_by("month")
        )

        interventions_month = list(
            FilterService.get_interventions_queryset(filters)
            .annotate(month=MonthKey("date_action"))
            .values("month")
            .annotate(total=Count("id_action_interv"))
            .order_by("month")
        )

        return {
            "incidents_month": incidents_month,
            "interventions_month": interventions_month,
        }
