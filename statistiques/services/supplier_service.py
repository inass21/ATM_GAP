from django.db.models import Count

from gab.models import Fournisseur, GAB
from gab.models_source import NewIncidentGab

from .filter_service import FilterService


class SupplierService:

    @staticmethod
    def get_supplier_statistics():

        suppliers = []

        for fournisseur in Fournisseur.objects.all():

            gabs =         FilterService.get_gabs_queryset().filter(
                fournisseur=fournisseur
            )

            terminals = gabs.values_list(
                "terminal",
                flat=True
            )

            total_gabs = gabs.count()

            operational = gabs.filter(
                etat=GAB.ETAT_OPERATIONNEL
            ).count()

            incidents = FilterService.get_incidents_queryset().filter(
                id_gab__in=terminals
            ).count()

            availability = (
                round(
                    (operational / total_gabs) * 100,
                    2,
                )
                if total_gabs
                else 0
            )

            suppliers.append({

                "supplier": fournisseur.nom_fournisseur,

                "gabs": total_gabs,

                "incidents": incidents,

                "availability": availability,

            })

        suppliers.sort(
            key=lambda x: (
                x["availability"],
                -x["incidents"],
            ),
            reverse=True,
        )

        return suppliers
    
    @staticmethod
    def get_best_supplier():

        suppliers = (
            SupplierService
            .get_supplier_statistics()
        )

        if not suppliers:
            return None

        return suppliers[0]
    
    @staticmethod
    def get_supplier_distribution():

        suppliers = (
            FilterService.get_incidents_queryset()
            .values("cd_fournisseur")
            .annotate(
                incidents=Count("id_incident")
            )
            .order_by("-incidents")
        )

        return suppliers
    @staticmethod
    def get_supplier_summary():

        suppliers = (
            SupplierService
            .get_supplier_statistics()
        )

        return {

            "suppliers": suppliers,

            "best_supplier": (
                SupplierService
                .get_best_supplier()
            ),

            "distribution": (
                SupplierService
                .get_supplier_distribution()
            ),

        }