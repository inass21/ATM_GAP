from django.db.models import Count
from gab.models_source import (
    NewCategorieIntervention,
    NewIncidentGab,
)
from django.db.models import (
    Avg,
    DurationField,
    ExpressionWrapper,
    F,
)

from .filter_service import FilterService


class CategoryService:

    @staticmethod
    def get_category_distribution():

        categories = (
            FilterService.get_incidents_queryset()
            .values("id_categories_technique")
            .annotate(
                total=Count("id_incident")
            )
            .order_by("-total")
        )

        total_incidents = sum(
            category["total"]
            for category in categories
        )

        results = []

        for category in categories:

            category_name = (
                NewCategorieIntervention.objects.filter(
                    id_categorie=category["id_categories_technique"]
                )
                .values_list(
                    "libelle",
                    flat=True,
                )
                .first()
            )

            percentage = (
                round(
                    (category["total"] / total_incidents) * 100,
                    2,
                )
                if total_incidents
                else 0
            )

            results.append({

                "id": category["id_categories_technique"],

                "category": category_name or "Non définie",

                "incidents": category["total"],

                "percentage": percentage,

            })

        return results
    @staticmethod
    def get_category_mttr():

        categories = (
            FilterService.get_incidents_queryset()
            .exclude(date_remise__isnull=True)
            .values("id_categories_technique")
            .annotate(
                incidents=Count("id_incident"),
                mttr=Avg(
                    ExpressionWrapper(
                        F("date_remise") - F("date_arrete"),
                        output_field=DurationField(),
                    )
                ),
            )
            .order_by("-incidents")
        )

        results = []

        for category in categories:

            category_name = (
                NewCategorieIntervention.objects.filter(
                    id_categorie=category["id_categories_technique"]
                )
                .values_list(
                    "libelle",
                    flat=True,
                )
                .first()
            )

            results.append({

                "id": category["id_categories_technique"],

                "category": category_name or "Non définie",

                "incidents": category["incidents"],

                "mttr": category["mttr"],

            })

        return results
    
    @staticmethod
    def get_top_categories(limit=5):

        return (
            CategoryService
            .get_category_distribution()
        )[:limit]
    @staticmethod
    def get_category_summary():

        distribution = (
            CategoryService
            .get_category_distribution()
        )

        mttr = (
            CategoryService
            .get_category_mttr()
        )

        return {

            "distribution": distribution,

            "mttr": mttr,

            "top_categories": distribution[:5],

            "total_categories": len(distribution),

        }

