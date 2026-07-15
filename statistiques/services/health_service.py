from django.db.models import Avg

from gab.models import GAB
from gab.models_source import (
    NewIncidentGab,
    NewInteventionIncident,
)

from .filter_service import FilterService


class HealthService:

    @staticmethod
    def get_health_scores():

        health_scores = []

        for gab in FilterService.get_gabs_queryset():

            score = 100

            incidents = FilterService.get_incidents_queryset({"atm": gab.terminal}).count()

            interventions = FilterService.get_interventions_queryset({"atm": gab.terminal}).count()

            average_escalation = (
                FilterService.get_interventions_queryset({"atm": gab.terminal})
                .aggregate(
                    value=Avg("nbr_escalade")
                )["value"]
                or 0
            )

            if gab.etat == GAB.ETAT_HORS_SERVICE:
                score -= 30

            elif gab.etat == GAB.ETAT_CRITIQUE:
                score -= 20

            elif gab.etat == GAB.ETAT_PASSIF:
                score -= 10

            score -= min(incidents, 25)

            score -= min(interventions // 5, 20)

            score -= min(int(average_escalation * 2), 10)

            score = max(score, 0)

            if score >= 90:
                status = "Excellent"

            elif score >= 75:
                status = "Bon"

            elif score >= 50:
                status = "Moyen"

            else:
                status = "Critique"

            health_scores.append({

                "terminal": gab.terminal,

                "nom": gab.nom_gab,

                "ville": gab.ville,

                "agence": gab.libelle_agence,

                "etat": gab.get_etat_display(),

                "incidents": incidents,

                "interventions": interventions,

                "score": score,

                "status": status,

            })

        health_scores.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        return health_scores