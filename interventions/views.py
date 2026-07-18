from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from statistiques.services.statistics_service import (
    StatisticsService,
)


class InterventionsListView(LoginRequiredMixin, TemplateView):

    login_url = "/login/"

    template_name = "interventions/liste.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["statistics"] = (
            StatisticsService.get_dashboard_statistics()
        )

        context["page_title"] = "Interventions"

        context["active_menu"] = "interventions"

        return context
