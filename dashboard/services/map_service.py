from django.db.models import Count

from gab.models import GAB
from gab.models_source import NewIncidentGab
from gab.services.availability import AvailabilityService

from statistiques.services.filter_service import FilterService


class MapService:

    # Indicateurs de supervision uniquement (pas de Health Score).
    GREEN_THRESHOLD = 75
    ORANGE_THRESHOLD = 50

    @classmethod
    def get_regions_summary(cls, filters=None):

        # Regroupement direct par GAB.ville (filiales de supervision).
        # Tous les GAB sont inclus, meme sans incident (pas de deduction,
        # pas de fallback, pas de dependance a NewIncidentGab pour la region).

        gabs = (
            FilterService.get_gabs_queryset(filters)
            .exclude(ville__isnull=True)
            .exclude(ville="")
            .values("ville", "terminal", "etat")
        )

        # ville -> {gab_ids, etat counts}
        villes = {}

        for row in gabs:

            ville = row["ville"]
            data = villes.setdefault(ville, {
                "gab_ids": [],
                "total_gab": 0,
                "operational_gab": 0,
                "offline_gab": 0,
            })

            data["gab_ids"].append(row["terminal"])
            data["total_gab"] += 1

            if row["etat"] == GAB.ETAT_OPERATIONNEL:
                data["operational_gab"] += 1
            elif row["etat"] == GAB.ETAT_HORS_SERVICE:
                data["offline_gab"] += 1

        all_terminal_ids = [
            tid for d in villes.values() for tid in d["gab_ids"]
        ]

        # 1 seule requete groupee pour les incidents ouverts par GAB.
        open_incidents_by_gab = dict(
            NewIncidentGab.objects
            .filter(etat_incident=0)
            .filter(id_gab__in=all_terminal_ids)
            .values_list("id_gab")
            .annotate(total=Count("id_incident"))
        )

        # 1 seule requete groupee pour la disponibilite : tous les incidents
        # lies aux GAB concernes, agreges par ville via la logique unique
        # de AvailabilityService (Single Source of Truth, pas de N+1).
        availability_by_ville = cls._availability_by_ville(
            all_terminal_ids, villes
        )

        summary = []

        for ville in sorted(villes.keys()):

            data = villes[ville]

            open_incidents = sum(
                open_incidents_by_gab.get(tid, 0)
                for tid in data["gab_ids"]
            )

            availability = availability_by_ville.get(ville, 100.0)

            color = cls._compute_color(availability)

            summary.append({
                "ville": ville,
                "total_gab": data["total_gab"],
                "operational_gab": data["operational_gab"],
                "offline_gab": data["offline_gab"],
                "open_incidents": open_incidents,
                "availability": availability,
                "color": color,
            })

        return summary

    @classmethod
    def _availability_by_ville(cls, terminal_ids, villes):

        # Reutilise la logique unique de AvailabilityService (pas de copie
        # de la formule). 1 seule requete groupee, pas de N+1.

        if not terminal_ids:
            return {}

        incidents = (
            NewIncidentGab.objects
            .filter(id_gab__in=terminal_ids)
        )

        terminal_to_ville = {
            tid: ville
            for ville, d in villes.items()
            for tid in d["gab_ids"]
        }

        # Queryset d'incidents par ville, puis calcul via AvailabilityService.
        result = {}

        for ville, data in villes.items():

            gab_ids = data["gab_ids"]
            gab_count = len(gab_ids)

            ville_incidents = incidents.filter(id_gab__in=gab_ids)

            result[ville] = AvailabilityService.get_availability(
                ville_incidents,
                gab_count=gab_count,
            )

        return result

    @classmethod
    def _compute_color(cls, availability):

        if availability >= cls.GREEN_THRESHOLD:
            return "green"
        if availability >= cls.ORANGE_THRESHOLD:
            return "orange"
        return "red"
