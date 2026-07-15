from .analytics_service import AnalyticsService
from .decision_service import DecisionService
from .distribution_service import DistributionService
from .evolution_service import EvolutionService
from .health_service import HealthService
from .kpi_service import KPIService
from .ranking_service import RankingService
from .sla_service import SLAService


class StatisticsService:

    @staticmethod
    def get_dashboard_statistics():

        return {

            "kpis": KPIService.get_kpis(),

            "distribution": DistributionService.get_distribution(),

            "evolution": EvolutionService.get_evolution(),

            "analytics": AnalyticsService.get_performance(),

            "health": HealthService.get_health_scores(),

            "rankings": {

                "gabs": RankingService.get_top_gabs(),

                "fournisseurs": RankingService.get_top_fournisseurs(),

                "agences": RankingService.get_top_agences(),

                "villes": RankingService.get_top_villes(),

            },

            "sla": SLAService.get_sla_metrics(),

            "recommendations": DecisionService.get_recommendations(),

        }