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

        # P2 : le Health Score est calcule UNE SEULE fois par requete puis
        # reutilise partout (Single Source of Truth). Evite 3 recalculs
        # redondants du meme traitement (health, health_global,
        # rankings.gabs, recommendations).
        health_scores = HealthService.get_health_scores(filters)

        # Meme principe pour les KPI et le SLA : calcules une seule fois puis
        # reutilises (dans le dict retourne ET par DecisionService), au lieu
        # d'etre recalcules a l'interieur de get_recommendations.
        kpis = KPIService.get_kpis(filters)

        sla = SLAService.get_sla_metrics(filters)

        return {

            "kpis": kpis,

            "distribution": DistributionService.get_distribution(filters),

            "evolution": EvolutionService.get_evolution(filters),

            "analytics": AnalyticsService.get_performance(filters),

            "health": health_scores,

            "health_global": HealthService.get_global_health(
                filters, scores=health_scores
            ),

            "rankings": {

                "gabs": RankingService.get_top_gabs(
                    filters=filters, scores=health_scores
                ),

                "fournisseurs": RankingService.get_top_fournisseurs(filters),

                "agences": RankingService.get_top_agences(filters=filters),

                "villes": RankingService.get_top_villes(filters=filters),

            },

            "sla": sla,

            "recommendations": DecisionService.get_recommendations(
                filters,
                scores=health_scores,
                kpis=kpis,
                sla=sla,
            ),

        }