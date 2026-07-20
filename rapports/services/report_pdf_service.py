import logging

from django.conf import settings
from django.template.loader import render_to_string

from weasyprint import HTML

from .report_data_service import ReportDataService
from .report_chart_service import ReportChartService


logger = logging.getLogger(__name__)


class ReportPDFGenerationError(Exception):
    """Levée quand la génération du PDF du rapport échoue."""


class ReportPDFService:

    TEMPLATE_NAME = "rapports/pdf/report_template.html"

    @classmethod
    def generate_pdf(
        cls,
        type_rapport,
        date_debut=None,
        date_fin=None,
    ) -> bytes:
        try:
            context = ReportDataService.build_report_context(
                type_rapport, date_debut, date_fin
            )
            charts = ReportChartService.build_report_charts(context)
            context["charts"] = charts

            html = render_to_string(cls.TEMPLATE_NAME, context)

            pdf_bytes = HTML(
                string=html,
                base_url=str(settings.BASE_DIR),
            ).write_pdf()

            if not pdf_bytes:
                raise ReportPDFGenerationError(
                    "WeasyPrint n'a produit aucun contenu PDF."
                )

            return pdf_bytes

        except ReportPDFGenerationError:
            raise
        except Exception as exc:
            logger.exception(
                "Échec de la génération du rapport PDF (%s) : %s",
                type_rapport,
                exc,
            )
            raise ReportPDFGenerationError(
                f"Échec de la génération du rapport PDF ({type_rapport}) : {exc}"
            ) from exc
