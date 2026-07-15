from django.db.models import Count

from gab.models import GAB, Fournisseur
from gab.models_source import (
    NewIncidentGab,
    NewInteventionIncident,
)

from .filter_service import FilterService


class DistributionService:

    @staticmethod
    def get_distribution(filters=None):

        etat_distribution = list(
            FilterService.get_gabs_queryset(filters)
            .values("etat")
            .annotate(total=Count("terminal"))
            .order_by("etat")
        )

        ville_distribution = list(
            FilterService.get_gabs_queryset(filters)
            .exclude(ville__isnull=True)
            .exclude(ville="")
            .values("ville")
            .annotate(total=Count("terminal"))
            .order_by("-total")
        )

        fournisseur_distribution = list(
            Fournisseur.objects
            .annotate(total=Count("gabs"))
            .values(
                "nom_fournisseur",
                "total",
            )
            .order_by("-total")
        )

        type_distribution = list(
            FilterService.get_gabs_queryset(filters)
            .exclude(type_gab__isnull=True)
            .exclude(type_gab="")
            .values("type_gab")
            .annotate(total=Count("terminal"))
            .order_by("-total")
        )

        agence_distribution = list(
            FilterService.get_gabs_queryset(filters)
            .exclude(libelle_agence__isnull=True)
            .exclude(libelle_agence="")
            .values("libelle_agence")
            .annotate(total=Count("terminal"))
            .order_by("-total")
        )[:10]

        incidents_filiale = list(
            FilterService.get_incidents_queryset(filters)
            .values("cd_filiale")
            .annotate(total=Count("id_incident"))
            .order_by("-total")
        )

        incidents_fournisseur = list(
            FilterService.get_incidents_queryset(filters)
            .values("cd_fournisseur")
            .annotate(total=Count("id_incident"))
            .order_by("-total")
        )

        interventions_responsable = list(
            FilterService.get_interventions_queryset(filters)
            .values("responsable")
            .annotate(total=Count("id_action_interv"))
            .order_by("-total")
        )

        return {

            "etat_distribution": etat_distribution,

            "ville_distribution": ville_distribution,

            "fournisseur_distribution": fournisseur_distribution,

            "type_distribution": type_distribution,

            "agence_distribution": agence_distribution,

            "incidents_filiale": incidents_filiale,

            "incidents_fournisseur": incidents_fournisseur,

            "interventions_responsable": interventions_responsable,

        }