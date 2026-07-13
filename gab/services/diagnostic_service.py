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

            if result:

                decision = DecisionEngine.evaluate(
                    result["action_id"],
                    result["etat_cloture"],
                )

                result.update(decision)

                components.append(result)

                availability = AvailabilityService.get_summary(
            gab_id
        )

        general_status = "Opérationnel"

        for component in components:

            if (
                component["severity"] == "Critique"
                and component["status"] != "Résolu"
            ):
                general_status = "En panne"
                break

            elif (
                component["severity"] == "Moyenne"
                and component["status"] != "Résolu"
            ):
                general_status = "Attention"

        history = HistoryService.get_history(gab_id)

        return {
            "gab_id": gab_id,
            "gab": gab_info,
            "general_status": general_status,
            "availability": availability,
            "components": components,
            "history": history,
        }