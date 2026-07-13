from django.utils import timezone

from gab.models_source import (
    NewIncidentGab,
    NewInteventionIncident,
)


class AvailabilityService:

    @staticmethod
    def get_summary(gab_id):

        incidents = NewIncidentGab.objects.filter(
            id_gab=gab_id
        )

        incident_count = incidents.count()

        open_incidents = incidents.filter(
            etat_incident=0
        ).count()

        closed_incidents = incidents.filter(
            etat_incident=1
        ).count()

        last_incident = (
            incidents.order_by("-id_incident")
            .first()
        )

        last_intervention = (
            NewInteventionIncident.objects.filter(
                id_gab=gab_id
            )
            .order_by("-date_action")
            .values_list("date_action", flat=True)
            .first()
        )

        availability = 100.0

        downtime = {
            "days": 0,
            "hours": 0,
            "minutes": 0,
            "display": "0 jour 0 heure 0 minute",
        }

        if (
            last_incident
            and last_incident.date_arrete
            and open_incidents > 0
        ):

            delta = timezone.now() - last_incident.date_arrete

            total_seconds = int(delta.total_seconds())

            days = total_seconds // 86400
            hours = (total_seconds % 86400) // 3600
            minutes = (total_seconds % 3600) // 60

            downtime = {
                "days": days,
                "hours": hours,
                "minutes": minutes,
                "display": f"{days} jours {hours} heures {minutes} minutes",
            }

        return {
            "incident_count": incident_count,
            "open_incidents": open_incidents,
            "closed_incidents": closed_incidents,
            "availability": availability,
            "downtime": downtime,
            "last_incident": (
                last_incident.id_incident
                if last_incident
                else None
            ),
            "last_intervention": last_intervention,
        }