from datetime import timedelta

from django.utils import timezone

from gab.models_source import (
    NewIncidentGab,
    NewInteventionIncident,
)


class AvailabilityService:

    WINDOW_DAYS = 30

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

        availability = AvailabilityService._compute_availability(incidents)

        downtime = {
            "days": 0,
            "hours": 0,
            "minutes": 0,
            "display": "0 jour 0 heure 0 minute",
        }

        open_incident = (
            incidents
            .filter(etat_incident=0)
            .order_by("date_arrete")
            .first()
        )

        if (
            open_incident
            and open_incident.date_arrete
        ):

            delta = timezone.now() - open_incident.date_arrete

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

    @staticmethod
    def _compute_availability(incidents):

        now = timezone.now()
        window_start = now - timedelta(days=AvailabilityService.WINDOW_DAYS)
        total_window = AvailabilityService.WINDOW_DAYS * 86400

        intervals = []

        for incident in incidents.filter(date_arrete__isnull=False):

            arrete = incident.date_arrete

            if arrete > now:
                continue

            if incident.etat_incident == 0:

                # Incident ouvert : indisponibilité en cours jusqu'à maintenant.
                start = arrete if arrete >= window_start else window_start
                end = now

            else:

                # Incident clôturé : on ne compte que si la remise en service
                # est cohérente (présente, postérieure à l'arrêt et <= maintenant).
                remise = incident.date_remise

                if not remise or remise > now or remise <= arrete:
                    continue

                start = arrete if arrete >= window_start else window_start
                end = remise

            if end > start:
                intervals.append((start, end))

        downtime_total = AvailabilityService._merge_downtime(
            intervals,
            window_start,
            now,
        )

        availability = 100.0 * (total_window - downtime_total) / total_window

        return round(max(0.0, min(100.0, availability)), 1)

    @staticmethod
    def _merge_downtime(intervals, window_start, now):

        if not intervals:
            return 0.0

        intervals.sort(key=lambda iv: iv[0])

        merged_start, merged_end = intervals[0]

        total_seconds = 0.0

        for start, end in intervals[1:]:

            if start <= merged_end:
                if end > merged_end:
                    merged_end = end
            else:
                total_seconds += (merged_end - merged_start).total_seconds()
                merged_start, merged_end = start, end

        total_seconds += (merged_end - merged_start).total_seconds()

        return total_seconds
