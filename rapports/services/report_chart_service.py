import base64
import io

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


class ReportChartDimensionError(ValueError):
    """Levée quand les listes passées à un graphique ont des dimensions incohérentes."""


class ReportChartService:

    PALETTE = ["#1e3a8a", "#10b981", "#ef4444", "#f59e0b", "#64748b", "#8b5cf6"]
    DANGER = "#ef4444"
    SUCCESS = "#10b981"
    PRIMARY = "#1e3a8a"

    _NO_DATA_TEXT = "Pas de données"

    @staticmethod
    def _render(fig):
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png", dpi=110, bbox_inches="tight")
        plt.close(fig)
        buffer.seek(0)
        encoded = base64.b64encode(buffer.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"

    @staticmethod
    def _empty_axis(ax, title):
        ax.text(0.5, 0.5, ReportChartService._NO_DATA_TEXT, ha="center", va="center", color=ReportChartService.PRIMARY)
        ax.set_title(title, fontsize=10, color=ReportChartService.PRIMARY)
        return ReportChartService._render(ax.get_figure())

    @classmethod
    def _assert_same_length(cls, *sequences, chart_name):
        lengths = {len(s) for s in sequences}
        if len(lengths) > 1:
            raise ReportChartDimensionError(
                f"[{chart_name}] dimensions incohérentes : "
                f"longueurs = {[len(s) for s in sequences]}"
            )
        if any(len(s) == 0 for s in sequences):
            raise ReportChartDimensionError(
                f"[{chart_name}] liste vide détectée : "
                f"longueurs = {[len(s) for s in sequences]}"
            )

    @classmethod
    def _safe_bar(cls, ax, labels, values, color, chart_name):
        cls._assert_same_length(labels, values, chart_name=chart_name)
        ax.bar(labels, values, color=color)

    @classmethod
    def _safe_barh(cls, ax, labels, values, color, chart_name):
        cls._assert_same_length(labels, values, chart_name=chart_name)
        ax.barh(labels, values, color=color)

    @classmethod
    def _safe_plot(cls, ax, x, y, chart_name, **kwargs):
        cls._assert_same_length(x, y, chart_name=chart_name)
        ax.plot(x, y, **kwargs)

    @classmethod
    def _safe_pie(cls, ax, values, chart_name, **kwargs):
        if not values:
            raise ReportChartDimensionError(
                f"[{chart_name}] aucune valeur fournie à plt.pie()"
            )
        ax.pie(values, **kwargs)

    @classmethod
    def generate_availability_chart(cls, context):
        evolution = (context.get("charts") or {}).get("evolution") or {}
        incidents_month = evolution.get("incidents_month") or []
        interventions_month = evolution.get("interventions_month") or []

        fig, ax = plt.subplots(figsize=(5, 3))
        incident_map = {row["month"]: row["total"] for row in incidents_month}
        intervention_map = {row["month"]: row["total"] for row in interventions_month}
        labels = sorted(set(incident_map) | set(intervention_map))

        if labels:
            incident_values = [incident_map.get(m, 0) for m in labels]
            intervention_values = [intervention_map.get(m, 0) for m in labels]
            cls._assert_same_length(
                labels, incident_values, intervention_values,
                chart_name="availability_chart",
            )
            cls._safe_plot(
                ax, labels, incident_values,
                chart_name="availability_chart",
                marker="o", color=cls.DANGER, label="Incidents",
            )
            cls._safe_plot(
                ax, labels, intervention_values,
                chart_name="availability_chart",
                marker="s", color=cls.SUCCESS, label="Interventions",
            )
            ax.set_ylim(bottom=0)
        else:
            ax.text(0.5, 0.5, cls._NO_DATA_TEXT, ha="center", va="center", color=cls.PRIMARY)
        ax.set_title("Évolution de la Disponibilité", fontsize=10, color=cls.PRIMARY)
        ax.legend(fontsize=7)
        ax.tick_params(labelsize=7)
        ax.grid(True, alpha=0.3)
        return cls._render(fig)

    @classmethod
    def generate_state_distribution_chart(cls, context):
        distribution = (context.get("charts") or {}).get("distribution") or {}
        etat_distribution = distribution.get("etat_distribution") or []

        fig, ax = plt.subplots(figsize=(5, 3))
        labels = [row["etat"] or "Inconnu" for row in etat_distribution]
        values = [row["total"] for row in etat_distribution]

        if labels:
            cls._assert_same_length(labels, values, chart_name="state_distribution_chart")
            cls._safe_pie(
                ax, values,
                chart_name="state_distribution_chart",
                labels=labels,
                autopct="%1.1f%%",
                colors=cls.PALETTE,
                textprops={"fontsize": 7},
            )
        else:
            ax.text(0.5, 0.5, cls._NO_DATA_TEXT, ha="center", va="center", color=cls.PRIMARY)
        ax.set_title("Répartition des États", fontsize=10, color=cls.PRIMARY)
        return cls._render(fig)

    @classmethod
    def generate_incidents_priority_chart(cls, context):
        evolution = (context.get("charts") or {}).get("evolution") or {}
        incidents_month = evolution.get("incidents_month") or []

        fig, ax = plt.subplots(figsize=(6, 3))
        labels = [row["month"] for row in incidents_month]
        values = [row["total"] for row in incidents_month]

        if labels:
            cls._assert_same_length(labels, values, chart_name="incidents_priority_chart")
            cls._safe_bar(ax, labels, values, cls.DANGER, chart_name="incidents_priority_chart")
            ax.set_ylim(bottom=0)
        else:
            ax.text(0.5, 0.5, cls._NO_DATA_TEXT, ha="center", va="center", color=cls.PRIMARY)
        ax.set_title("Évolution des Incidents par Priorité", fontsize=10, color=cls.PRIMARY)
        ax.tick_params(labelsize=7)
        ax.grid(True, axis="y", alpha=0.3)
        return cls._render(fig)

    @classmethod
    def generate_root_cause_chart(cls, context):
        distribution = (context.get("charts") or {}).get("distribution") or {}
        incidents_categorie = distribution.get("incidents_categorie") or []

        fig, ax = plt.subplots(figsize=(5, 3))
        labels = [row["categorie"] for row in incidents_categorie][:8]
        values = [row["total"] for row in incidents_categorie][:8]

        if labels:
            cls._assert_same_length(labels, values, chart_name="root_cause_chart")
            cls._safe_barh(
                ax, labels[::-1], values[::-1], cls.PRIMARY, chart_name="root_cause_chart"
            )
            ax.set_xlim(left=0)
        else:
            ax.text(0.5, 0.5, cls._NO_DATA_TEXT, ha="center", va="center", color=cls.PRIMARY)
        ax.set_title("Répartition par Cause Racine", fontsize=10, color=cls.PRIMARY)
        ax.tick_params(labelsize=7)
        ax.grid(True, axis="x", alpha=0.3)
        return cls._render(fig)

    @classmethod
    def generate_intervention_chart(cls, context):
        evolution = (context.get("charts") or {}).get("evolution") or {}
        interventions_month = evolution.get("interventions_month") or []

        fig, ax = plt.subplots(figsize=(5, 3))
        labels = [row["month"] for row in interventions_month]
        values = [row["total"] for row in interventions_month]

        if labels:
            cls._assert_same_length(labels, values, chart_name="intervention_chart")
            ax.fill_between(labels, values, color=cls.SUCCESS, alpha=0.4)
            cls._safe_plot(
                ax, labels, values,
                chart_name="intervention_chart",
                color=cls.SUCCESS, marker="o",
            )
            ax.set_ylim(bottom=0)
        else:
            ax.text(0.5, 0.5, cls._NO_DATA_TEXT, ha="center", va="center", color=cls.PRIMARY)
        ax.set_title("Volume d'Interventions", fontsize=10, color=cls.PRIMARY)
        ax.tick_params(labelsize=7)
        ax.grid(True, alpha=0.3)
        return cls._render(fig)

    @classmethod
    def build_report_charts(cls, context):
        charts = context.get("charts") or {}
        rankings = charts.get("rankings") or {}
        return {
            "availability_chart": cls.generate_availability_chart(context),
            "state_distribution_chart": cls.generate_state_distribution_chart(context),
            "priority_chart": cls.generate_incidents_priority_chart(context),
            "root_cause_chart": cls.generate_root_cause_chart(context),
            "intervention_chart": cls.generate_intervention_chart(context),
            "rankings": rankings,
        }
