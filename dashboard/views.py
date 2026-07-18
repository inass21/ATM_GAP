from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from dashboard.services.dashboard_service import (
    DashboardService,
)
from dashboard.services.map_service import (
    MapService,
)


class DashboardView(LoginRequiredMixin, TemplateView):

    login_url = "/login/"

    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # Source unique de verite : DashboardService orchestre les services
        # existants (KPIService, HealthService, EvolutionService, MapService).
        # Aucune donnee fictive.
        context["dashboard"] = DashboardService.get_context()

        context["page_title"] = "Supervision Parc GAB"

        context["active_menu"] = "dashboard"

        return context


class CarteView(LoginRequiredMixin, TemplateView):

    login_url = "/login/"

    template_name = "dashboard/carte.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # Supervision nationale : reutilise MapService (Single Source of Truth),
        # sans recalcul de la disponibilite par ville.
        context["regions"] = MapService.get_regions_summary()

        context["page_title"] = "Carte de supervision"

        context["active_menu"] = "carte"

        return context


class DeclarationIncidentView(LoginRequiredMixin, TemplateView):

    login_url = "/login/"

    template_name = "dashboard/declaration_incident.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["page_title"] = "Déclaration d'incident"

        context["active_menu"] = "incidents"

        return context
