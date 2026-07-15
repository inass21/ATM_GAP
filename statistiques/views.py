from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .services.business_intelligence_service import (
    BusinessIntelligenceService,
)
from .services.statistics_service import (
    StatisticsService,
)


class StatisticsDashboardView(
    LoginRequiredMixin,
    TemplateView,
):

    login_url = "/login/"

    template_name = "statistiques/dashboard.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["statistics"] = (
            StatisticsService.get_dashboard_statistics()
        )

        context["business"] = (
            BusinessIntelligenceService.get_business_report()
        )

        context["page_title"] = "Statistiques"

        context["active_menu"] = "statistiques"

        return context