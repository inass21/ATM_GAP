import unicodedata

from gab.models import GAB
from gab.models_source import (
    NewIncidentGab,
    NewInteventionIncident,
)


_ALIASES = {
    "date_from": "date_from",
    "date_debut": "date_from",
    "date_to": "date_to",
    "date_fin": "date_to",
    "fournisseur": "fournisseur",
    "supplier": "fournisseur",
    "filiale": "filiale",
    "region": "region",
    "agence": "agence",
    "agency": "agence",
    "ville": "ville",
    "city": "ville",
    "categorie_technique": "categorie_technique",
    "categorie": "categorie_technique",
    "category": "categorie_technique",
    "categorie_fonctionnelle": "categorie_fonctionnelle",
    "etat_gab": "etat_gab",
    "etat": "etat_gab",
    "etat_incident": "etat_incident",
    "atm": "atm",
    "terminal": "atm",
}


def _normalize_key(key):

    key = unicodedata.normalize("NFKD", str(key))
    key = "".join(
        c for c in key if not unicodedata.combining(c)
    )
    return key.lower().strip().replace(" ", "_").replace("-", "_")


def _normalize_filters(filters):

    if not filters:
        return {}

    normalized = {}

    for raw_key, value in filters.items():

        if value is None or value == "":
            continue

        canonical = _ALIASES.get(_normalize_key(raw_key))

        if canonical:
            normalized[canonical] = value

    return normalized


def _present(value):
    return value is not None and value != ""


class FilterService:

    # GAB

    @staticmethod
    def get_gabs_queryset(filters=None):

        queryset = GAB.objects.all()

        filters = _normalize_filters(filters)

        if not filters:
            return queryset

        if _present(filters.get("date_from")):
            queryset = queryset.filter(
                derniere_synchronisation__gte=filters["date_from"]
            )

        if _present(filters.get("date_to")):
            queryset = queryset.filter(
                derniere_synchronisation__lte=filters["date_to"]
            )

        if _present(filters.get("fournisseur")):
            queryset = queryset.filter(
                fournisseur_id=filters["fournisseur"]
            )

        if _present(filters.get("agence")):
            queryset = queryset.filter(
                code_agence=filters["agence"]
            )

        if _present(filters.get("ville")):
            queryset = queryset.filter(
                ville__icontains=filters["ville"]
            )

        if _present(filters.get("etat_gab")):
            queryset = queryset.filter(
                etat=filters["etat_gab"]
            )

        if _present(filters.get("atm")):
            queryset = queryset.filter(
                terminal=filters["atm"]
            )

        return queryset

    # Incidents (NewIncidentGab)
    @staticmethod
    def get_incidents_queryset(filters=None):

        queryset = NewIncidentGab.objects.all()

        filters = _normalize_filters(filters)

        if not filters:
            return queryset

        if _present(filters.get("date_from")):
            queryset = queryset.filter(
                date_arrete__gte=filters["date_from"]
            )

        if _present(filters.get("date_to")):
            queryset = queryset.filter(
                date_arrete__lte=filters["date_to"]
            )

        if _present(filters.get("fournisseur")):
            queryset = queryset.filter(
                cd_fournisseur=filters["fournisseur"]
            )

        if _present(filters.get("filiale")):
            queryset = queryset.filter(
                cd_filiale=filters["filiale"]
            )

        if _present(filters.get("region")):
            queryset = queryset.filter(
                cd_region=filters["region"]
            )

        if _present(filters.get("agence")):
            queryset = queryset.filter(
                cd_agence=filters["agence"]
            )

        if _present(filters.get("ville")):
            queryset = queryset.filter(
                id_gab__in=GAB.objects.filter(
                    ville=filters["ville"]
                ).values("terminal")
            )

        if _present(filters.get("categorie_technique")):
            queryset = queryset.filter(
                id_categories_technique=filters["categorie_technique"]
            )

        if _present(filters.get("categorie_fonctionnelle")):
            queryset = queryset.filter(
                id_categories_fonctionnelle=filters["categorie_fonctionnelle"]
            )

        if filters.get("etat_incident") is not None:
            queryset = queryset.filter(
                etat_incident=filters["etat_incident"]
            )

        if _present(filters.get("atm")):
            queryset = queryset.filter(
                id_gab=filters["atm"]
            )

        return queryset
    # Interventions (NewInteventionIncident)
    @staticmethod
    def get_interventions_queryset(filters=None):

        queryset = NewInteventionIncident.objects.all()

        filters = _normalize_filters(filters)

        if not filters:
            return queryset

        if _present(filters.get("date_from")):
            queryset = queryset.filter(
                date_action__gte=filters["date_from"]
            )

        if _present(filters.get("date_to")):
            queryset = queryset.filter(
                date_action__lte=filters["date_to"]
            )

        if _present(filters.get("fournisseur")):
            queryset = queryset.filter(
                id_fournisseur=filters["fournisseur"]
            )

        if _present(filters.get("region")):
            queryset = queryset.filter(
                cd_region_iprc=filters["region"]
            )

        if _present(filters.get("agence")):
            queryset = queryset.filter(
                cd_agence=filters["agence"]
            )

        if _present(filters.get("ville")):
            queryset = queryset.filter(
                id_gab__in=GAB.objects.filter(
                    ville=filters["ville"]
                ).values("terminal")
            )

        if _present(filters.get("categorie_technique")):
            queryset = queryset.filter(
                id_categories=filters["categorie_technique"]
            )

        if filters.get("etat_incident") is not None:
            queryset = queryset.filter(
                etat_cloture=filters["etat_incident"]
            )

        if _present(filters.get("atm")):
            queryset = queryset.filter(
                id_gab=filters["atm"]
            )

        return queryset
