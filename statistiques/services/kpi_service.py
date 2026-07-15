from gab.models import GAB, Fournisseur
from gab.models_source import (
    NewIncidentGab,
    NewInteventionIncident,
)
from utilisateurs.models import Filiale

from .filter_service import FilterService


class KPIService:

    @staticmethod
    def get_kpis():

        total_gab =         FilterService.get_gabs_queryset().count()

        operational_gab =         FilterService.get_gabs_queryset().filter(
            etat=GAB.ETAT_OPERATIONNEL
        ).count()

        critical_gab =         FilterService.get_gabs_queryset().filter(
            etat=GAB.ETAT_CRITIQUE
        ).count()

        offline_gab =         FilterService.get_gabs_queryset().filter(
            etat=GAB.ETAT_HORS_SERVICE
        ).count()

        passive_gab =         FilterService.get_gabs_queryset().filter(
            etat=GAB.ETAT_PASSIF
        ).count()

        total_incidents = FilterService.get_incidents_queryset().count()

        total_interventions = (
            FilterService.get_interventions_queryset().count()
        )

        total_filiales = Filiale.objects.count()

        total_fournisseurs = Fournisseur.objects.count()

        availability = round(
            (operational_gab / total_gab) * 100,
            1,
        ) if total_gab else 0

        return {
            "total_gab": total_gab,
            "operational_gab": operational_gab,
            "critical_gab": critical_gab,
            "offline_gab": offline_gab,
            "passive_gab": passive_gab,
            "total_incidents": total_incidents,
            "total_interventions": total_interventions,
            "total_filiales": total_filiales,
            "total_fournisseurs": total_fournisseurs,
            "availability": availability,
        }