from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from statistiques.services.statistics_service import (
    StatisticsService,
)


class IncidentsListView(LoginRequiredMixin, TemplateView):

    login_url = "/login/"

    template_name = "incidents/liste.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["statistics"] = (
            StatisticsService.get_dashboard_statistics()
        )

        context["page_title"] = "Incidents"

        context["active_menu"] = "incidents"

        return context
