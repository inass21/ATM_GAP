from gab.models_source import (
    NewInteventionIncident,
    NewActionIntervention,
)

from .constants import COMPONENT_ACTIONS


class ComponentStatusService:

    @staticmethod
    def get_status(gab_id: int, component: str):

        action_ids = COMPONENT_ACTIONS.get(component)

        if not action_ids:
            return None

        intervention = (
            NewInteventionIncident.objects.filter(
                id_gab=gab_id,
                id_action_intervention__in=action_ids
            )
            .order_by("-date_action")
            .first()
        )

        if intervention is None:
            return {
                "component": component,
                "status": "Inconnu",
                "action_id": None,
                "action": None,
                "date": None,
                "etat_cloture": None,
            }

        action = (
            NewActionIntervention.objects.filter(
                id_intevention=intervention.id_action_intervention
            ).first()
        )

        if intervention.etat_cloture == 1:
            status = "Traité"
        else:
            status = "À traiter"

        return {
            "component": component,
            "status": status,
            "action_id": intervention.id_action_intervention,
            "action": action.libelle_intevention if action else None,
            "date": intervention.date_action,
            "etat_cloture": intervention.etat_cloture,
        }