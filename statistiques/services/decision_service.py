from .health_service import HealthService
from .sla_service import SLAService
from .ranking_service import RankingService
from .kpi_service import KPIService
from .category_service import CategoryService
from .supplier_service import SupplierService


class DecisionService:

    @staticmethod
    def get_recommendations(filters=None, scores=None, kpis=None, sla=None):

        recommendations = []

        if kpis is None:
            kpis = KPIService.get_kpis(filters)

        if sla is None:
            sla = SLAService.get_sla_metrics(filters)

        if scores is None:
            scores = HealthService.get_health_scores(filters)

        health = scores

        top_gabs = RankingService.get_top_gabs(5, filters, scores=scores)

        if kpis["availability"] < 95:

            recommendations.append({
                "level": "danger",
                "title": "Disponibilité faible",
                "message": (
                    f"La disponibilité globale est de "
                    f'{kpis["availability"]}%.'
                ),
            })

        if sla["sla_rate"] < 90:

            recommendations.append({
                "level": "warning",
                "title": "SLA",
                "message": (
                    f'Seulement {sla["sla_rate"]}% '
                    "des incidents respectent le SLA."
                ),
            })

        if top_gabs:

            worst = min(
                top_gabs,
                key=lambda x: x["score"]
            )

            if worst["score"] < 60:

                recommendations.append({

                    "level": "danger",

                    "title": "ATM critique",

                    "message": (
                        f'{worst["terminal"]} '
                        "nécessite une maintenance."
                    ),

                })

        critical = len([
            gab for gab in health
            if gab["status"] == "Critique"
        ])

        if critical:

            recommendations.append({

                "level": "warning",

                "title": "ATM critiques",

                "message": (
                    f"{critical} ATM sont "
                    "dans un état critique."
                ),

            })

        if not recommendations:

            recommendations.append({

                "level": "success",

                "title": "Plateforme",

                "message": (
                    "Tous les indicateurs sont "
                    "dans les seuils."
                ),

            })

        return recommendations

    @staticmethod
    def get_executive_insights():

        insights = []

        kpis = KPIService.get_kpis()

        supplier = SupplierService.get_best_supplier()

        categories = (
            CategoryService
            .get_top_categories(1)
        )

        if kpis["availability"] < 95:

            insights.append({

                "type": "danger",

                "title": "Disponibilité",

                "message": (
                    f"La disponibilité globale est "
                    f"{kpis['availability']}%."
                ),

            })

        if supplier:

            insights.append({

                "type": "success",

                "title": "Fournisseur",

                "message": (
                    f"{supplier['supplier']} possède "
                    "la meilleure disponibilité."
                ),

            })

        if categories:

            insights.append({

                "type": "warning",

                "title": "Catégorie dominante",

                "message": (
                    f"{categories[0]['category']} "
                    "génère le plus d'incidents."
                ),

            })

        return insights

    @staticmethod
    def get_operational_score():

        kpis = KPIService.get_kpis()

        score = 100

        score -= kpis["offline_gab"] * 2

        score -= kpis["critical_gab"]

        score -= max(
            0,
            95 - kpis["availability"]
        )

        score = max(0, score)

        if score >= 90:
            status = "Excellent"

        elif score >= 75:
            status = "Bon"

        elif score >= 60:
            status = "Moyen"

        else:
            status = "Critique"

        return {

            "score": score,

            "status": status,

        }

    @staticmethod
    def get_network_health():

        health = (
            HealthService
            .get_health_scores()
        )

        if not health:

            return 0

        average = sum(

            item["score"]

            for item in health

        ) / len(health)

        return round(
            average,
            2,
        )

    @staticmethod
    def get_risk_level():

        kpis = KPIService.get_kpis()

        sla = SLAService.get_sla_metrics()

        health = HealthService.get_health_scores()

        score = 0

        if kpis["availability"] < 95:
            score += 30

        if sla["sla_rate"] < 90:
            score += 25

        critical = len([
            item
            for item in health
            if item["score"] < 60
        ])

        score += critical * 5

        if score >= 70:
            level = "Élevé"

        elif score >= 40:
            level = "Moyen"

        else:
            level = "Faible"

        return {

            "score": score,

            "level": level,

        }

    @staticmethod
    def get_business_rules():

        rules = []

        kpis = KPIService.get_kpis()

        sla = SLAService.get_sla_metrics()

        categories = CategoryService.get_top_categories(1)

        supplier = SupplierService.get_best_supplier()

        if kpis["availability"] < 95:

            rules.append({

                "severity": "danger",

                "title": "Disponibilité",

                "message": (
                    "La disponibilité globale "
                    "est inférieure à 95%."
                ),

            })

        if sla["sla_rate"] < 90:

            rules.append({

                "severity": "warning",

                "title": "SLA",

                "message": (
                    "Le SLA est inférieur "
                    "à l'objectif."
                ),

            })

        if categories:

            if categories[0]["percentage"] > 40:

                rules.append({

                    "severity": "warning",

                    "title": "Catégorie dominante",

                    "message": (
                        f"{categories[0]['category']} "
                        "génère une forte proportion "
                        "des incidents."
                    ),

                })

        if supplier:

            if supplier["availability"] < 90:

                rules.append({

                    "severity": "danger",

                    "title": "Fournisseur",

                    "message": (
                        f"{supplier['supplier']} "
                        "présente une faible disponibilité."
                    ),

                })

        return rules

    @staticmethod
    def get_decision_dashboard():

        return {

            "recommendations": (
                DecisionService
                .get_recommendations()
            ),

            "insights": (
                DecisionService
                .get_executive_insights()
            ),

            "business_rules": (
                DecisionService
                .get_business_rules()
            ),

            "risk": (
                DecisionService
                .get_risk_level()
            ),

            "operational_score": (
                DecisionService
                .get_operational_score()
            ),

            "network_health": (
                DecisionService
                .get_network_health()
            ),

        }
