from django.db.models import (
    Avg,
    DurationField,
    ExpressionWrapper,
    F,
)

from gab.models_source import NewIncidentGab

from .filter_service import FilterService


class SLAService:

    @staticmethod
    def get_sla_metrics():

        incidents = FilterService.get_incidents_queryset()

        total_incidents = incidents.count()

        closed_incidents = incidents.exclude(
            date_remise__isnull=True
        )

        closed_count = closed_incidents.count()

        mttr = (
            closed_incidents
            .annotate(
                duration=ExpressionWrapper(
                    F("date_remise") - F("date_arrete"),
                    output_field=DurationField(),
                )
            )
            .aggregate(
                value=Avg("duration")
            )["value"]
        )

        response_time = (
            incidents.exclude(
                date_prise_en_charge__isnull=True
            )
            .annotate(
                duration=ExpressionWrapper(
                    F("date_prise_en_charge") - F("date_arrete"),
                    output_field=DurationField(),
                )
            )
            .aggregate(
                value=Avg("duration")
            )["value"]
        )

        sla_respected = incidents.filter(
            date_prise_en_charge__lte=F(
                "date_prise_en_charge_contractuelle"
            )
        ).count()

        sla_not_respected = total_incidents - sla_respected

        sla_rate = (
            round(
                (sla_respected / total_incidents) * 100,
                2,
            )
            if total_incidents
            else 0
        )

        return {

            "total_incidents": total_incidents,

            "closed_incidents": closed_count,

            "mttr": mttr,

            "mean_response_time": response_time,

            "sla_respected": sla_respected,

            "sla_not_respected": sla_not_respected,

            "sla_rate": sla_rate,

        }