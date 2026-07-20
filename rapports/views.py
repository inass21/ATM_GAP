from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView

from .services.report_pdf_service import ReportPDFService, ReportPDFGenerationError


class RapportsListView(LoginRequiredMixin, TemplateView):

    login_url = "/login/"

    template_name = "rapports/liste.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Rapports"
        context["active_menu"] = "rapports"
        return context


class TestPDFView(LoginRequiredMixin, View):

    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        type_rapport = request.GET.get("type", "global")
        date_debut = request.GET.get("date_debut")
        date_fin = request.GET.get("date_fin")
        try:
            pdf = ReportPDFService.generate_pdf(type_rapport, date_debut, date_fin)
        except ReportPDFGenerationError as exc:
            return HttpResponse(f"Erreur de génération PDF : {exc}", status=500)
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'inline; filename="rapport_{type_rapport}.pdf"'
        )
        return response
