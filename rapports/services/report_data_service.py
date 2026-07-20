from django.utils import timezone

from statistiques.services.statistics_service import StatisticsService
from statistiques.services.kpi_service import KPIService
from statistiques.services.filter_service import FilterService


class ReportDataService:

    _GAB_FIELDS = [
        "terminal",
        "numero_serie",
        "nom_gab",
        "libelle_agence",
        "ville",
        "etat",
        "type_gab",
        "fournisseur_id",
        "derniere_synchronisation",
    ]

    _INCIDENT_FIELDS = [
        "id_incident",
        "id_gab",
        "num_tiket",
        "num_affectation",
        "date_arrete",
        "etat_incident",
        "cd_filiale",
        "cd_region",
        "cd_agence",
        "nom_agence",
        "cd_fournisseur",
        "id_categories_technique",
        "id_categories_fonctionnelle",
    ]

    _INTERVENTION_FIELDS = [
        "id_action_interv",
        "id_incident",
        "id_gab",
        "nomgab",
        "cd_agence",
        "nom_agence",
        "cd_region_iprc",
        "id_fournisseur",
        "id_categories",
        "date_action",
        "etat_cloture",
        "date_cloture",
        "motif_cloture",
    ]

    @staticmethod
    def _build_filters(date_debut=None, date_fin=None):
        filters = {}
        if date_debut:
            filters["date_debut"] = date_debut
        if date_fin:
            filters["date_fin"] = date_fin
        return filters or None

    @staticmethod
    def _generate_report_title(type_rapport, date_debut, date_fin):
        period = ""
        if date_debut and date_fin:
            period = f" ({date_debut} au {date_fin})"
        elif date_debut:
            period = f" (à partir du {date_debut})"
        elif date_fin:
            period = f" (jusqu'au {date_fin})"
        return f"Rapport {type_rapport}{period}"

    @staticmethod
    def get_dashboard_kpis(date_debut=None, date_fin=None):
        filters = ReportDataService._build_filters(date_debut, date_fin)
        return KPIService.get_kpis(filters)

    @staticmethod
    def get_incident_statistics(date_debut=None, date_fin=None, statistics=None):
        filters = ReportDataService._build_filters(date_debut, date_fin)
        if statistics is None:
            statistics = StatisticsService.get_dashboard_statistics(filters)
        incidents_qs = FilterService.get_incidents_queryset(filters)
        return {
            "statistics": statistics,
            "incidents": list(incidents_qs.values(*ReportDataService._INCIDENT_FIELDS)),
            "total": incidents_qs.count(),
            "ouverts": incidents_qs.filter(etat_incident=0).count(),
            "clotures": incidents_qs.filter(etat_incident=1).count(),
        }

    @staticmethod
    def get_gab_statistics(date_debut=None, date_fin=None, statistics=None):
        filters = ReportDataService._build_filters(date_debut, date_fin)
        if statistics is None:
            statistics = StatisticsService.get_dashboard_statistics(filters)
        gabs_qs = FilterService.get_gabs_queryset(filters)
        return {
            "statistics": statistics,
            "gabs": list(gabs_qs.values(*ReportDataService._GAB_FIELDS)),
            "total": gabs_qs.count(),
        }

    @staticmethod
    def get_intervention_statistics(date_debut=None, date_fin=None, statistics=None):
        filters = ReportDataService._build_filters(date_debut, date_fin)
        if statistics is None:
            statistics = StatisticsService.get_dashboard_statistics(filters)
        interventions_qs = FilterService.get_interventions_queryset(filters)
        return {
            "statistics": statistics,
            "interventions": list(interventions_qs.values(*ReportDataService._INTERVENTION_FIELDS)),
            "total": interventions_qs.count(),
            "en_cours": interventions_qs.filter(etat_cloture=0).count(),
            "cloturees": interventions_qs.filter(etat_cloture=1).count(),
        }

    @staticmethod
    def get_charts(date_debut=None, date_fin=None, statistics=None):
        if statistics is None:
            filters = ReportDataService._build_filters(date_debut, date_fin)
            statistics = StatisticsService.get_dashboard_statistics(filters)
        return {
            "distribution": statistics.get("distribution"),
            "evolution": statistics.get("evolution"),
            "analytics": statistics.get("analytics"),
            "health": statistics.get("health"),
            "sla": statistics.get("sla"),
            "rankings": statistics.get("rankings"),
        }

    @staticmethod
    def build_report_context(type_rapport, date_debut=None, date_fin=None):
        statistics = StatisticsService.get_dashboard_statistics(
            ReportDataService._build_filters(date_debut, date_fin)
        )

        kpis = ReportDataService.get_dashboard_kpis(date_debut, date_fin)
        gab = ReportDataService.get_gab_statistics(date_debut, date_fin, statistics)
        incidents = ReportDataService.get_incident_statistics(date_debut, date_fin, statistics)
        interventions = ReportDataService.get_intervention_statistics(date_debut, date_fin, statistics)
        charts = ReportDataService.get_charts(date_debut, date_fin, statistics)

        report_info = {
            "type_rapport": type_rapport,
            "titre": ReportDataService._generate_report_title(
                type_rapport, date_debut, date_fin
            ),
            "version": "1.0",
            "generated_by": None,
            "date_debut": date_debut,
            "date_fin": date_fin,
            "date_generation": timezone.now(),
        }

        return {
            "report_info": report_info,
            "kpis": kpis,
            "gab": gab,
            "incidents": incidents,
            "interventions": interventions,
            "charts": charts,
        }
