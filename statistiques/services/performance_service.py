from django.db.models import Avg, DurationField, ExpressionWrapper, F

from gab.models_source import (
    NewIncidentGab,
    NewInteventionIncident,
)

from .filter_service import FilterService


class PerformanceService:

    @staticmethod
    def get_performance_metrics():

        closed_incidents = (
            FilterService.get_incidents_queryset()
            .exclude(date_arrete__isnull=True)
            .exclude(date_remise__isnull=True)
            .filter(etat_incident=1)
        )

        mttr = (
            closed_incidents
            .annotate(
                duration=ExpressionWrapper(
                    F("date_remise") - F("date_arrete"),
                    output_field=DurationField(),
                )
            )
            .aggregate(
                average=Avg("duration")
            )["average"]
        )

        response_time = (
            closed_incidents
            .exclude(date_prise_en_charge__isnull=True)
            .annotate(
                duration=ExpressionWrapper(
                    F("date_prise_en_charge") - F("date_arrete"),
                    output_field=DurationField(),
                )
            )
            .aggregate(
                average=Avg("duration")
            )["average"]
        )

        intervention_time = (
            FilterService.get_interventions_queryset()
            .exclude(date_action__isnull=True)
            .exclude(date_prise_en_charge__isnull=True)
            .annotate(
                duration=ExpressionWrapper(
                    F("date_action") - F("date_prise_en_charge"),
                    output_field=DurationField(),
                )
            )
            .aggregate(
                average=Avg("duration")
            )["average"]
        )

        total_incidents = FilterService.get_incidents_queryset().count()

        closed_count = closed_incidents.count()

        closing_rate = (
            round((closed_count / total_incidents) * 100, 2)
            if total_incidents else 0
        )

        escalation = (
            FilterService.get_interventions_queryset().aggregate(
                average=Avg("nbr_escalade")
            )["average"]
            or 0
        )

        relance = (
            FilterService.get_interventions_queryset().aggregate(
                average=Avg("nbr_tentative")
            )["average"]
            
            or 0
        )

        return {
            "mttr": mttr,
            "mean_response_time": response_time,
            "mean_intervention_time": intervention_time,
            "closing_rate": closing_rate,
            "average_escalation": round(escalation, 2),
            "average_relance": round(relance, 2),
        }