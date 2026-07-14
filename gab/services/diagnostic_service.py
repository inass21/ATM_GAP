from django.utils import timezone

from gab.models import GAB

from .component_status import ComponentStatusService
from .availability import AvailabilityService

from gab.rules.decision_engine import DecisionEngine
from .history_service import HistoryService


class DiagnosticService:

    COMPONENTS = [
        "card_reader",
        "printer",
        "epp",
        "shutter",
        "cash_dispenser",
        "connection",
    ]

    @classmethod
    def get_diagnostic(cls, gab_id):
        return cls._get_diagnostic_from_db(gab_id)

    @classmethod
    def _get_diagnostic_from_db(cls, gab_id):

        gab = (
            GAB.objects
            .select_related("fournisseur")
            .filter(terminal=gab_id)
            .first()
        )

        gab_info = None

        if gab:
            gab_info = {
                "terminal": gab.terminal,
                "nom": gab.nom_gab,
                "agence": gab.libelle_agence,
                "ville": gab.ville,
                "numero_serie": gab.numero_serie,
                "fournisseur": (
                    gab.fournisseur.nom_fournisseur
                    if gab.fournisseur
                    else None
                ),
            }

        components = []

        for component in cls.COMPONENTS:

            result = ComponentStatusService.get_status(
                gab_id,
                component,
            )

            if not result:
                continue

            if result["action_id"] is None:

                components.append({
                    "component": component,
                    "status": "Inconnu",
                    "severity": "Inconnu",
                    "action": None,
                    "cause": None,
                    "recommendation": None,
                    "support_contact": None,
                    "etat_cloture": None,
                    "date": None,
                })
                continue

            decision = DecisionEngine.evaluate(
                result["action_id"],
                result["etat_cloture"],
            )

            components.append({
                "component": component,
                "status": decision["status"],
                "severity": decision["severity"],
                "action": result["action"],
                "cause": decision["cause"],
                "recommendation": decision["recommendation"],
                "support_contact": decision["support_contact"],
                "etat_cloture": result["etat_cloture"],
                "date": result["date"],
            })

        availability = AvailabilityService.get_summary(gab_id)

        general_status = cls._compute_general_status(
            gab.etat if gab else None,
            components,
        )

        history = HistoryService.get_history(gab_id)

        return {
            "gab_id": gab_id,
            "gab": gab_info,
            "general_status": general_status,
            "availability": availability,
            "components": components,
            "history": history,
        }

    @classmethod
    def _compute_general_status(cls, gab_etat, components):

        if gab_etat == GAB.ETAT_PASSIF:
            return "Passif"

        if gab_etat in (GAB.ETAT_HORS_SERVICE, GAB.ETAT_CRITIQUE):
            return "En panne"

        general_status = "Opérationnel"

        for component in components:

            if (
                component["severity"] == "Critique"
                and component["status"] != "Résolu"
            ):
                return "En panne"

            if (
                component["severity"] == "Moyenne"
                and component["status"] != "Résolu"
            ):
                general_status = "Attention"

        return general_status

    @classmethod
    def get_default_component(cls, diagnostic):
        components = diagnostic.get("components") or []

        if not components:
            return None

        severity_rank = {
            "Critique": 3,
            "Moyenne": 2,
            "Faible": 1,
            "Inconnu": 0,
        }

        epoch = timezone.now().replace(
            year=1970,
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        def sort_date(component):
            date = component.get("date")
            return date if date is not None else epoch

        def is_open(component):
            if component.get("etat_cloture") == 1:
                return False

            status = component.get("status")

            return status not in (
                "Opérationnel",
                "Résolu",
                "Inconnu",
            )

        open_components = [c for c in components if is_open(c)]

        if open_components:
            open_components.sort(
                key=lambda c: (
                    severity_rank.get(c.get("severity"), 0),
                    sort_date(c),
                ),
                reverse=True,
            )

            return open_components[0]["component"]

        resolved = [c for c in components if c.get("etat_cloture") == 1]

        if resolved:
            resolved.sort(key=sort_date, reverse=True)

            return resolved[0]["component"]

        return components[0]["component"]
