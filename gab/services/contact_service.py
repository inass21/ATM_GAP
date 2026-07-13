from gab.models_source import NewLibelleTypeContact


class ContactService:

    @staticmethod
    def get_contact(libelle):

        contact = (
            NewLibelleTypeContact.objects
            .filter(libelle__iexact=libelle)
            .first()
        )

        if not contact:
            return None

        return {

            "support": contact.libelle,

            "responsable": contact.contact_nom,

            "telephone": contact.gsm_contact,

            "email": contact.aa_mail,

            "cc": contact.cc_mail,

            "sla": contact.duree_sla,

            "heure_debut": str(contact.born_debut_contrac),

            "heure_fin": str(contact.born_fin_contrac),

        }