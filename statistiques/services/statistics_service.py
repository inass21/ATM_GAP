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
    def get_dashboard_statistics(filters=None):

        return {

            "kpis": KPIService.get_kpis(filters),

            "distribution": DistributionService.get_distribution(filters),

            "evolution": EvolutionService.get_evolution(filters),

            "analytics": AnalyticsService.get_performance(filters),

            "health": HealthService.get_health_scores(filters),

            "rankings": {

                "gabs": RankingService.get_top_gabs(filters=filters),

                "fournisseurs": RankingService.get_top_fournisseurs(filters),

                "agences": RankingService.get_top_agences(filters=filters),

                "villes": RankingService.get_top_villes(filters=filters),

            },

            "sla": SLAService.get_sla_metrics(filters),

            "recommendations": DecisionService.get_recommendations(filters),

        }