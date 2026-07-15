from django.db.models import Count
from gab.models import GAB
from django.db.models import (
    Avg,
    DurationField,
    ExpressionWrapper,
    F,
)

from gab.models_source import (
    NewIncidentGab,
    NewInteventionIncident,
)
from .filter_service import FilterService
class AnalyticsService:
    @staticmethod
    def get_performance():

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
                value=Avg("duration")
            )["value"]
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
                value=Avg("duration")
            )["value"]
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
                value=Avg("duration")
            )["value"]
        )

        total_incidents = FilterService.get_incidents_queryset().count()

        closed_count = closed_incidents.count()

        closing_rate = (
            (closed_count / total_incidents) * 100
            if total_incidents
            else 0
        )


        average_escalation = (
            FilterService.get_interventions_queryset().aggregate(
                value=Avg("nbr_escalade")
            )["value"]
            or 0
        )


        average_relance = (
            FilterService.get_interventions_queryset().aggregate(
                value=Avg("nbr_tentative")
            )["value"]
            or 0
        )

        return {
            "mttr": mttr,
            "mean_response_time": response_time,      
            
            "mean_intervention_time": intervention_time,
            "closing_rate": round(closing_rate, 2),
            "average_escalation": round(average_escalation, 2),
            "average_relance": round(average_relance, 2),
        }

    @staticmethod
    def get_health_score():

        health = []

        gabs = FilterService.get_gabs_queryset()

        for gab in gabs:

            score = 100

            incidents = FilterService.get_incidents_queryset({"atm": gab.terminal}).count()

            interventions = FilterService.get_interventions_queryset({"atm": gab.terminal}).count()

            escalades = (
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

            score -= min(int(escalades * 2), 10)

            score = max(score, 0)

            if score >= 90:
                level = "Excellent"

            elif score >= 75:
                level = "Bon"

            elif score >= 50:
                level = "Moyen"

            else:
                level = "Critique"

            health.append({
                "terminal": gab.terminal,
                "nom": gab.nom_gab,
                "agence": gab.libelle_agence,
                "ville": gab.ville,
                "etat": gab.get_etat_display(),
                "score": score,
                "level": level,
            })

        health.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        return health
    
    @staticmethod
    def get_top_gabs(limit=10):

        gabs = FilterService.get_gabs_queryset()

        ranking = []

        for gab in gabs:

            incidents = (
                FilterService.get_incidents_queryset().filter(
                    id_gab__in=terminals
                ).count()
            )

            interventions = (
                FilterService.get_interventions_queryset().filter(
                    id_gab__in=terminals
                ).count()
            )

            ranking.append({

                "terminal": gab.terminal,

                "nom": gab.nom_gab,

                "agence": gab.libelle_agence,

                "ville": gab.ville,

                "etat": gab.get_etat_display(),

                "incidents": incidents,

                "interventions": interventions,

            })

        ranking.sort(
            key=lambda x: (
                x["incidents"],
                x["interventions"],
            ),
            reverse=True,
        )

        return ranking[:limit]
    
    @staticmethod
    def get_top_fournisseurs():

        fournisseurs = FilterService.get_gabs_queryset().values(
            "fournisseur__nom_fournisseur"
        ).annotate(
            total_gab=Count("terminal")
        )

        ranking = []

        for fournisseur in fournisseurs:

            nom = fournisseur["fournisseur__nom_fournisseur"]

            gabs = FilterService.get_gabs_queryset().filter(
                fournisseur__nom_fournisseur=nom
            )

            terminals = gabs.values_list(
                "terminal",
                flat=True,
            )

            incidents = (
                FilterService.get_incidents_queryset().filter(
                    id_gab__in=terminals
                ).count()
            )

            interventions = (
                FilterService.get_interventions_queryset().filter(
                    id_gab__in=terminals
                ).count()
            )

            operational = gabs.filter(
                etat=GAB.ETAT_OPERATIONNEL
            ).count()

            total = gabs.count()

            availability = (
                round((operational / total) * 100, 1)
                if total else 0
            )

            ranking.append({

                "nom": nom,

                "total_gab": total,

                "incidents": incidents,

                "interventions": interventions,

                "availability": availability,

            })

        ranking.sort(
            key=lambda x: (
                x["availability"],
                -x["incidents"],
            ),
            reverse=True,
        )

        return ranking
    @staticmethod
    def get_top_agences(limit=10):

        agences = (
            FilterService.get_gabs_queryset()
            .exclude(libelle_agence__isnull=True)
            .exclude(libelle_agence="")
            .values("libelle_agence")
            .annotate(
                total_gab=Count("terminal")
            )
        )

        ranking = []

        for agence in agences:

            nom = agence["libelle_agence"]

            gabs = FilterService.get_gabs_queryset().filter(
                libelle_agence=nom
            )

            terminals = gabs.values_list(
                "terminal",
                flat=True,
            )

            incidents = (
                FilterService.get_incidents_queryset().filter(
                    id_gab__in=terminals
                ).count()
            )

            interventions = (
                FilterService.get_interventions_queryset().filter(
                    id_gab__in=terminals
                ).count()
            )

            operational = gabs.filter(
                etat=GAB.ETAT_OPERATIONNEL
            ).count()

            total = gabs.count()

            availability = (
                round((operational / total) * 100, 1)
                if total else 0
            )

            ranking.append({

                "agence": nom,

                "total_gab": total,

                "incidents": incidents,

                "interventions": interventions,

                "availability": availability,

            })

        ranking.sort(
            key=lambda x: (
                x["availability"],
                -x["incidents"],
            ),
            reverse=True,
        )

        return ranking[:limit]
    
    @staticmethod
    def get_top_villes(limit=10):

        villes = (
            FilterService.get_gabs_queryset()
            .exclude(ville__isnull=True)
            .exclude(ville="")
            .values("ville")
            .annotate(
                total_gab=Count("terminal")
            )
        )

        ranking = []

        for ville in villes:

            nom = ville["ville"]

            gabs = FilterService.get_gabs_queryset().filter(
                ville=nom
            )

            terminals = gabs.values_list(
                "terminal",
                flat=True,
            )

            incidents = (
                FilterService.get_incidents_queryset().filter(
                    id_gab__in=terminals
                ).count()
            )

            interventions = (
                FilterService.get_interventions_queryset().filter(
                    id_gab__in=terminals
                ).count()
            )

            operational = gabs.filter(
                etat=GAB.ETAT_OPERATIONNEL
            ).count()

            total = gabs.count()

            availability = (
                round((operational / total) * 100, 1)
                if total else 0
            )

            ranking.append({

                "ville": nom,

                "total_gab": total,

                "incidents": incidents,

                "interventions": interventions,

                "availability": availability,

            })

        ranking.sort(
            key=lambda x: (
                x["availability"],
                -x["incidents"],
            ),
            reverse=True,
        )

        return ranking[:limit]