from django.db.models import Count
from django.db.models.functions import TruncMonth

from gab.models_source import (
    NewIncidentGab,
    NewInteventionIncident,
)

from .filter_service import FilterService


class EvolutionService:

    @staticmethod
    def get_evolution(filters=None):

        incidents_month = list(
            FilterService.get_incidents_queryset(filters)
            .annotate(month=TruncMonth("date_arrete"))
            .values("month")
            .annotate(total=Count("id_incident"))
            .order_by("month")
        )

        interventions_month = list(
            FilterService.get_interventions_queryset(filters)
            .annotate(month=TruncMonth("date_action"))
            .values("month")
            .annotate(total=Count("id_action_interv"))
            .order_by("month")
        )

        return {
            "incidents_month": incidents_month,
            "interventions_month": interventions_month,
        }