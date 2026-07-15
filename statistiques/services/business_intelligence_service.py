from .category_service import CategoryService
from .decision_service import DecisionService
from .health_service import HealthService
from .kpi_service import KPIService
from .ranking_service import RankingService
from .sla_service import SLAService
from .supplier_service import SupplierService


class BusinessIntelligenceService:

    @staticmethod
    def get_executive_summary():

        kpis = KPIService.get_kpis()

        sla = SLAService.get_sla_metrics()

        health = HealthService.get_health_scores()

        average_health = 0

        if health:

            average_health = round(

                sum(
                    item["score"]
                    for item in health
                ) / len(health),

                2,

            )

        return {

            "availability": kpis["availability"],

            "total_gabs": kpis["total_gab"],

            "total_incidents": kpis["total_incidents"],

            "total_interventions": kpis["total_interventions"],

            "sla_rate": sla["sla_rate"],

            "mttr": sla["mttr"],

            "average_health": average_health,

        }

    @staticmethod
    def get_priorities():

        priorities = []

        health = HealthService.get_health_scores()

        for atm in health:

            if atm["score"] < 60:

                priorities.append({

                    "type": "ATM",

                    "label": atm["terminal"],

                    "reason": "Health Score faible",

                    "priority": "Haute",

                })

        return priorities

    @staticmethod
    def get_strengths():

        strengths = []

        supplier = SupplierService.get_best_supplier()

        if supplier:

            strengths.append({

                "title": "Meilleur fournisseur",

                "value": supplier["supplier"],

            })

        categories = CategoryService.get_top_categories(1)

        if categories:

            strengths.append({

                "title": "Catégorie dominante",

                "value": categories[0]["category"],

            })

        rankings = RankingService.get_top_gabs(1)

        if rankings:

            strengths.append({

                "title": "ATM le plus performant",

                "value": rankings[0]["terminal"],

            })

        return strengths

    @staticmethod
    def get_business_report():

        return {

            "summary": (
                BusinessIntelligenceService
                .get_executive_summary()
            ),

            "decision": (
                DecisionService
                .get_decision_dashboard()
            ),

            "strengths": (
                BusinessIntelligenceService
                .get_strengths()
            ),

            "priorities": (
                BusinessIntelligenceService
                .get_priorities()
            ),

        }