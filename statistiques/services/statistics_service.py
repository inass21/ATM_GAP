import hashlib
import json

from django.conf import settings
from django.core.cache import cache

from .analytics_service import AnalyticsService
from .decision_service import DecisionService
from .distribution_service import DistributionService
from .evolution_service import EvolutionService
from .health_service import HealthService
from .kpi_service import KPIService
from .ranking_service import RankingService
from .sla_service import SLAService


_STATS_CACHE_PREFIX = "asims:statistics:"


def _stats_cache_key(filters):
    # Cle stable a partir des filtres (meme filtres -> meme resultat cache).
    if not filters:
        return _STATS_CACHE_PREFIX + "all"
    payload = json.dumps(filters, sort_keys=True, default=str)
    digest = hashlib.md5(payload.encode("utf-8")).hexdigest()[:16]
    return _STATS_CACHE_PREFIX + digest


def invalidate_statistics_cache():
    """Vide le cache des statistiques (appele quand une donnee source change)."""
    try:
        cache.delete_pattern(_STATS_CACHE_PREFIX + "*")
    except AttributeError:
        # LocMemCache ne supporte pas delete_pattern : on vide le cache par
        # defaut. Les autres caches nommes ne sont pas utilises ici.
        cache.clear()


class StatisticsService:

    @staticmethod
    def get_dashboard_statistics(filters=None):

        # P0 : mise en cache du resultat lourd (par combinaison de filtres).
        # Evite de rescanner tout le parc a chaque chargement de page.
        cache_key = _stats_cache_key(filters)
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

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

        result = {

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

        cache.set(
            cache_key,
            result,
            getattr(settings, "STATISTICS_CACHE_TTL", 300),
        )

        return result
