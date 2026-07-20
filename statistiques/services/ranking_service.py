from django.db.models import Count

from gab.models import GAB, Fournisseur
from gab.models_source import (
    NewIncidentGab,
    NewInteventionIncident,
)

from .health_service import HealthService
from .filter_service import FilterService


class RankingService:

    @staticmethod
    def get_top_gabs(limit=10, filters=None, scores=None):

        if scores is None:
            scores = HealthService.get_health_scores(filters)

        # "Top GAB en panne" : les GAB les plus problématiques doivent
        # remonter en premier. Le score de santé décroît quand l'état est
        # dégradé et quand les incidents / interventions / escalades
        # augmentent : le plus faible score = le GAB le plus critique.
        # On trie donc par score CROISSANT (les pires d'abord).
        return sorted(
            scores,
            key=lambda x: x["score"],
        )[:limit]

    @staticmethod
    def get_top_fournisseurs(filters=None):

        ranking = []

        for fournisseur in Fournisseur.objects.all():

            gabs = FilterService.get_gabs_queryset(filters).filter(
                fournisseur=fournisseur
            )

            terminals = gabs.values_list(
                "terminal",
                flat=True,
            )

            total_gab = gabs.count()

            operational = gabs.filter(
                etat=GAB.ETAT_OPERATIONNEL
            ).count()

            incidents = FilterService.get_incidents_queryset(filters).filter(
                id_gab__in=terminals
            ).count()

            interventions = FilterService.get_interventions_queryset(filters).filter(
                id_gab__in=terminals
            ).count()

            availability = (
                round((operational / total_gab) * 100, 1)
                if total_gab else 0
            )

            ranking.append({

                "fournisseur": fournisseur.nom_fournisseur,

                "total_gab": total_gab,

                "incidents": incidents,

                "interventions": interventions,

                "availability": availability,

            })

        return sorted(
            ranking,
            key=lambda x: (
                x["availability"],
                -x["incidents"],
            ),
            reverse=True,
        )

    @staticmethod
    def get_top_agences(limit=10, filters=None):

        agences = list(
            FilterService.get_gabs_queryset(filters)
            .values("libelle_agence")
            .annotate(
                total=Count("terminal")
            )
        )

        incidents_qs = (
            FilterService.get_incidents_queryset(filters)
            .values("nom_agence")
            .annotate(
                incidents_majeurs=Count("id_incident")
            )
        )
        incidents_par_agence = {
            row["nom_agence"]: row["incidents_majeurs"]
            for row in incidents_qs
            if row["nom_agence"]
        }

        result = []
        for row in agences:
            nom = row["libelle_agence"] or "Inconnue"
            result.append({
                "libelle_agence": nom,
                "nom": nom,
                "total": row["total"],
                "nb_gab": row["total"],
                "incidents_majeurs": incidents_par_agence.get(nom, 0),
                "mttr": "-",
            })

        return sorted(
            result,
            key=lambda x: x["incidents_majeurs"],
            reverse=True,
        )[:limit]

    @staticmethod
    def get_top_villes(limit=10, filters=None):

        villes = (
            FilterService.get_gabs_queryset(filters)
            .values("ville")
            .annotate(
                total=Count("terminal")
            )
        )

        return sorted(
            villes,
            key=lambda x: x["total"],
            reverse=True,
        )[:limit]