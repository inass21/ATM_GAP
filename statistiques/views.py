from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .services.statistics_service import (
    StatisticsService,
)


class StatisticsDashboardView(
    LoginRequiredMixin,
    TemplateView,
):

    login_url = "/login/"

    template_name = "statistiques/dashboard.html"

    FILTER_FIELDS = {
        "date_debut": "date_from",
        "date_fin": "date_to",
        "region": "region",
        "filiale": "filiale",
        "agence": "agence",
        "ville": "ville",
        "fournisseur": "fournisseur",
        "categorie": "categorie_technique",
        "etat": "etat_gab",
        "atm": "atm",
    }

    FILTER_LABELS = {
        "date_debut": "Date début",
        "date_fin": "Date fin",
        "region": "Région",
        "filiale": "Filiale",
        "agence": "Agence",
        "ville": "Ville",
        "fournisseur": "Fournisseur",
        "categorie": "Catégorie",
        "etat": "État",
        "atm": "ATM",
    }

    def _build_filters(self):

        params = self.request.GET

        filters = {}
        selected_filters = []

        for field, canonical in self.FILTER_FIELDS.items():

            value = params.get(field)

            if value in (None, ""):
                continue

            filters[canonical] = value

            selected_filters.append({
                "field": field,
                "label": self.FILTER_LABELS[field],
                "value": value,
            })

        return filters, selected_filters

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        filters, selected_filters = self._build_filters()

        context["statistics"] = (
            StatisticsService.get_dashboard_statistics(filters)
        )

        context["filters"] = filters

        context["selected_filters"] = selected_filters

        context["page_title"] = "Statistiques"

        context["active_menu"] = "statistiques"

        return context
