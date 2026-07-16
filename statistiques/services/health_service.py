from django.db.models import Avg, Count

from gab.models import GAB
from gab.models_source import (
    NewIncidentGab,
    NewInteventionIncident,
)

from .filter_service import FilterService


class HealthService:

    @staticmethod
    def get_health_scores(filters=None):

        health_scores = []

        # P1 : agregations groupees (GROUP BY id_gab) au lieu de 3 requetes
        # par GAB. Le resultat est strictement equivalent au calcul unitaire
        # precedent (per_gab_filters = filters + atm=terminal), mais en 3
        # requetes au total au lieu de 3 * nombre de GAB.
        incidents_by_gab = dict(
            FilterService.get_incidents_queryset(filters)
            .values_list("id_gab")
            .annotate(total=Count("id_incident"))
        )

        interventions_by_gab = dict(
            FilterService.get_interventions_queryset(filters)
            .values_list("id_gab")
            .annotate(total=Count("id_action_interv"))
        )

        escalation_by_gab = dict(
            FilterService.get_interventions_queryset(filters)
            .values_list("id_gab")
            .annotate(value=Avg("nbr_escalade"))
        )

        for gab in FilterService.get_gabs_queryset(filters):

            score = 100

            incidents = incidents_by_gab.get(gab.terminal, 0)

            interventions = interventions_by_gab.get(gab.terminal, 0)

            average_escalation = escalation_by_gab.get(gab.terminal) or 0

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

    @staticmethod
    def get_global_health(filters=None, scores=None):

        if scores is None:
            scores = HealthService.get_health_scores(filters)

        if scores:
            global_score = round(
                sum(item["score"] for item in scores) / len(scores)
            )
        else:
            global_score = 0

        if global_score >= 90:
            global_status = "Excellent"
        elif global_score >= 75:
            global_status = "Bon"
        elif global_score >= 50:
            global_status = "Moyen"
        else:
            global_status = "Critique"

        return {
            "score": global_score,
            "status": global_status,
        }