from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import GAB, Fournisseur
from .services.diagnostic_service import DiagnosticService



def liste_gab(request):
    gabs = GAB.objects.select_related("fournisseur").all().order_by("terminal")

    terminal = request.GET.get("terminal")
    nom = request.GET.get("nom")
    fournisseur = request.GET.get("fournisseur")
    etat = request.GET.get("etat")
    ville = request.GET.get("ville")

    if terminal:
        gabs = gabs.filter(terminal__icontains=terminal)

    if nom:
        gabs = gabs.filter(nom_gab__icontains=nom)

    if fournisseur:
        gabs = gabs.filter(fournisseur_id=fournisseur)

    if etat:
        gabs = gabs.filter(etat=etat)

    if ville:
        gabs = gabs.filter(ville__icontains=ville)

    operational_count = gabs.filter(etat=GAB.ETAT_OPERATIONNEL).count()
    critical_count = gabs.filter(etat=GAB.ETAT_CRITIQUE).count()
    total_count = gabs.count()
    availability = round((operational_count / total_count) * 100, 1) if total_count else 0

    paginator = Paginator(gabs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop("page", None)

    context = {
        "page_obj": page_obj,
        "gabs": page_obj,
        "fournisseurs": Fournisseur.objects.all().order_by("nom_fournisseur"),
        "etats": GAB.ETAT_CHOICES,
        "query_string": query_params.urlencode(),
        "operational_count": operational_count,
        "critical_count": critical_count,
        "availability": availability,
    }

    return render(request, "gab/liste_gab.html", context)


def gab_api_detail(request, terminal):
    gab = get_object_or_404(GAB.objects.select_related("fournisseur"), terminal=terminal)
    return JsonResponse({
        "terminal": gab.terminal,
        "nom_gab": gab.nom_gab or "—",
        "ville": gab.ville or "—",
        "libelle_agence": gab.libelle_agence or "—",
        "fournisseur": gab.fournisseur.nom_fournisseur if gab.fournisseur else "—",
        "ip_adresse_gab": gab.ip_adresse_gab or "—",
        "etat": gab.etat,
        "etat_display": gab.get_etat_display(),
        "derniere_synchronisation": gab.derniere_synchronisation.strftime("%d/%m/%Y %H:%M") if gab.derniere_synchronisation else "—",
        "adresse_gab": gab.adresse_gab or "—",
        "type_gab": gab.type_gab or "—",
        "numero_serie": gab.numero_serie or "—",
        "code_agence": gab.code_agence or "—",
        "emplacement": gab.emplacement or "—",
    })

def diagnostic_api(request, gab_id):
    diagnostic = DiagnosticService.get_diagnostic(gab_id)

    return JsonResponse(diagnostic, safe=False)