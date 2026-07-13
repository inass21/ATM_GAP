from gab.models_source import (
    NewInteventionIncident,
    NewActionIntervention,
)

from gab.services.contact_service import ContactService


CATEGORY_CONTACT = {
    1: "NCR",
    4: "NCR",
    5: "Logistique",
    6: "Monétique",
    7: "TELECOM",
}


class HistoryService:

    @staticmethod
    def get_history(gab_id, limit=5):

        interventions = (
            NewInteventionIncident.objects
            .filter(id_gab=gab_id)
            .order_by("-date_action")[:limit]
        )

        history = []

        for intervention in interventions:

            action = (
                NewActionIntervention.objects
                .filter(
                    id_intevention=intervention.id_action_intervention
                )
                .first()
            )

            support = None

            if action:
                support = CATEGORY_CONTACT.get(
                    action.id_categories
                )

            contact = (
                ContactService.get_contact(support)
                if support
                else None
            )

            history.append({

                "date": intervention.date_action,

                "action": (
                    action.libelle_intevention
                    if action
                    else None
                ),

                "etat": (
                    "Résolu"
                    if intervention.etat_cloture == 1
                    else "En cours"
                ),

                "support": support,

                "contact": contact,

                "commentaire": intervention.commentaire,

            })

        return history