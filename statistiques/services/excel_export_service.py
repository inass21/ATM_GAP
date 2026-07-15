import json
from io import BytesIO

from django.http import HttpResponse
from django.utils import timezone
from openpyxl import Workbook

_INVALID_SHEET_CHARS = (":", "\\", "/", "?", "*", "[", "]")

_CONTENT_TYPE_XLSX = (
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


def _sanitize_sheet_name(name, fallback_index):

    name = str(name).strip()

    for char in _INVALID_SHEET_CHARS:
        name = name.replace(char, " ")

    name = name[:31].strip() or "Feuille{0}".format(fallback_index)

    return name


def _stringify(value):

    if value is None:
        return ""

    if isinstance(value, (dict, list)):
        try:
            return json.dumps(value, ensure_ascii=False, default=str)
        except TypeError:
            return str(value)

    return str(value)


def _rows_from_value(value):

    if value is None or isinstance(value, (str, int, float, bool)):
        return [[_stringify(value)]]

    if isinstance(value, dict):
        return [[str(key), _stringify(sub)] for key, sub in value.items()]

    if isinstance(value, list):

        if value and all(isinstance(item, dict) for item in value):

            keys = []

            for item in value:
                for key in item.keys():
                    if key not in keys:
                        keys.append(key)

            rows = [[str(key) for key in keys]]

            for item in value:
                rows.append([_stringify(item.get(key)) for key in keys])

            return rows

        return [[_stringify(item)] for item in value]

    return [[_stringify(value)]]


_REPORT_TITLE = "Rapport statistique des GAB"

_KPI_LABELS = (
    ("total_gab", "Total GAB"),
    ("operational_gab", "GAB opérationnels"),
    ("critical_gab", "GAB critiques"),
    ("offline_gab", "GAB hors service"),
    ("passive_gab", "GAB passifs"),
    ("total_incidents", "Total incidents"),
    ("total_interventions", "Total interventions"),
    ("total_filiales", "Total filiales"),
    ("total_fournisseurs", "Total fournisseurs"),
    ("availability", "Disponibilité (%)"),
)


def _build_executive_summary_lines(statistics):

    lines = []

    kpis = statistics.get("kpis") or {}
    sla = statistics.get("sla") or {}
    analytics = statistics.get("analytics") or {}
    health = statistics.get("health") or []
    recommendations = statistics.get("recommendations") or {}

    availability = kpis.get("availability")
    total_gab = kpis.get("total_gab")
    operational = kpis.get("operational_gab")
    critical = kpis.get("critical_gab")
    offline = kpis.get("offline_gab")
    total_incidents = kpis.get("total_incidents")
    total_interventions = kpis.get("total_interventions")

    if availability is not None:
        lines.append(
            "Disponibilite : la disponibilite globale du parc est de {0}% "
            "(sur {1} GAB, {2} operationnels, {3} critiques, {4} hors "
            "service).".format(
                availability,
                total_gab or 0,
                operational or 0,
                critical or 0,
                offline or 0,
            )
        )

    if total_incidents is not None:
        closed = sla.get("closed_incidents")
        lines.append(
            "Incidents : {0} incidents enregistres, {1} clôtures, pour "
            "{2} interventions.".format(
                total_incidents,
                closed or 0,
                total_interventions or 0,
            )
        )

    sla_rate = sla.get("sla_rate")
    if sla_rate is not None:
        lines.append(
            "SLA : le taux de respect du SLA est de {0}%.".format(sla_rate)
        )

    mttr = analytics.get("mttr")
    if mttr is not None:
        lines.append("MTTR moyen : {0}.".format(mttr))

    if health:
        critical_atms = [
            item for item in health
            if item.get("status") == "Critique"
        ]
        lines.append(
            "Sante du reseau : {0} GAB en etat critique sur {1}.".format(
                len(critical_atms),
                len(health),
            )
        )

    if recommendations:
        titles = ", ".join(
            item.get("title", "")
            for item in recommendations
            if item.get("title")
        )
        if titles:
            lines.append(
                "Recommandations : {0}.".format(titles)
            )

    if not lines:
        lines.append(
            "Aucune donnee statistique disponible pour generer le resume."
        )

    return lines


def _build_executive_summary_rows(statistics, filters):

    rows = []

    rows.append(["Resume Executif"])
    rows.append([])
    rows.append(["Titre du rapport", _REPORT_TITLE])
    rows.append([
        "Date et heure de generation",
        timezone.now().strftime("%d/%m/%Y %H:%M:%S"),
    ])

    rows.append([])
    rows.append(["Filtres appliques"])
    if filters:
        for key, value in filters.items():
            rows.append([str(key), _stringify(value)])
    else:
        rows.append(["(aucun filtre applique)"])

    rows.append([])
    rows.append(["KPIs principaux"])
    kpis = statistics.get("kpis") or {}
    for key, label in _KPI_LABELS:
        rows.append([label, _stringify(kpis.get(key))])

    rows.append([])
    rows.append(["Resume executif"])
    for line in _build_executive_summary_lines(statistics):
        rows.append([line])

    return rows


def _build_kpis_rows(statistics, filters):

    rows = []

    rows.append(["Indicateur", "Valeur"])

    kpis = statistics.get("kpis") or {}
    for key, label in _KPI_LABELS:
        rows.append([label, _stringify(kpis.get(key))])

    return rows


_RANKING_SECTIONS = (
    ("gabs", "Top GAB"),
    ("fournisseurs", "Top Fournisseurs"),
    ("agences", "Top Agences"),
    ("villes", "Top Villes"),
)


def _build_ranking_rows(statistics, filters):

    rows = []

    rankings = statistics.get("rankings") or {}

    for key, title in _RANKING_SECTIONS:

        rows.append([title])

        data = rankings.get(key)

        if data:
            rows.extend(_rows_from_value(data))
        else:
            rows.append(["(aucune donnee)"])

        rows.append([])

    return rows


_DISTRIBUTION_SECTIONS = (
    ("etat_distribution", "Distribution par etat"),
    ("ville_distribution", "Distribution par ville"),
    ("fournisseur_distribution", "Distribution par fournisseur"),
    ("type_distribution", "Distribution par type"),
    ("agence_distribution", "Distribution par agence"),
    ("incidents_filiale", "Incidents par filiale"),
    ("incidents_fournisseur", "Incidents par fournisseur"),
    ("interventions_responsable", "Interventions par responsable"),
)


def _build_distribution_rows(statistics, filters):

    rows = []

    distribution = statistics.get("distribution") or {}

    for key, title in _DISTRIBUTION_SECTIONS:

        rows.append([title])

        data = distribution.get(key)

        if data:
            rows.extend(_rows_from_value(data))
        else:
            rows.append(["(aucune donnee)"])

        rows.append([])

    return rows


_EVOLUTION_SECTIONS = (
    ("incidents_month", "Evolution des incidents par mois"),
    ("interventions_month", "Evolution des interventions par mois"),
)


def _build_evolution_rows(statistics, filters):

    rows = []

    evolution = statistics.get("evolution") or {}

    for key, title in _EVOLUTION_SECTIONS:

        rows.append([title])

        data = evolution.get(key)

        if data:
            rows.extend(_rows_from_value(data))
        else:
            rows.append(["(aucune donnee)"])

        rows.append([])

    return rows


def _build_health_rows(statistics, filters):

    rows = []

    health = statistics.get("health") or []

    if health:
        rows.extend(_rows_from_value(health))
    else:
        rows.append(["(aucune donnee)"])

    return rows


def _build_recommendations_rows(statistics, filters):

    rows = []

    recommendations = statistics.get("recommendations") or []

    if recommendations:
        rows.extend(_rows_from_value(recommendations))
    else:
        rows.append(["(aucune donnee)"])

    return rows


def _build_filters_rows(statistics, filters):

    return _rows_from_value(filters or {})


_SHEET_BUILDERS = (
    ("Résumé Exécutif", _build_executive_summary_rows, None),
    ("KPIs", _build_kpis_rows, "kpis"),
    ("Ranking", _build_ranking_rows, "rankings"),
    ("Filtres", _build_filters_rows, None),
    ("Distribution", _build_distribution_rows, "distribution"),
    ("Health", _build_health_rows, "health"),
    ("Evolution", _build_evolution_rows, "evolution"),
    ("Recommendations", _build_recommendations_rows, "recommendations"),
)


def _build_workbook(sheets):

    workbook = Workbook()
    workbook.remove(workbook.active)

    for index, (name, rows) in enumerate(sheets, start=1):
        worksheet = workbook.create_sheet(
            title=_sanitize_sheet_name(name, index)
        )
        for row in rows:
            worksheet.append([_stringify(cell) for cell in row])

    return workbook


class ExcelExportService:

    @staticmethod
    def export(statistics, filters=None):

        sheets = []

        claimed_sections = set()

        for name, builder, section in _SHEET_BUILDERS:
            sheets.append((name, builder(statistics, filters)))
            if section:
                claimed_sections.add(section)

        for section, data in statistics.items():
            if section in claimed_sections:
                continue
            sheets.append((section, _rows_from_value(data)))

        workbook = _build_workbook(sheets)

        buffer = BytesIO()
        workbook.save(buffer)

        response = HttpResponse(
            buffer.getvalue(), content_type=_CONTENT_TYPE_XLSX
        )
        response["Content-Disposition"] = (
            'attachment; filename="statistiques.xlsx"'
        )

        return response
