from gab.services.contact_service import ContactService


class DecisionEngine:

    RULES = {

        419: {
            "support": "TELECOM",
            "status": "En panne",
            "severity": "Critique",
            "cause": "Perte de communication réseau.",
            "recommendation": "Vérifier la connexion réseau."
        },

        434: {
            "support": "TELECOM",
            "status": "En panne",
            "severity": "Critique",
            "cause": "Communication interrompue.",
            "recommendation": "Contrôler la liaison réseau."
        },

        421: {
            "support": "NCR",
            "status": "En panne",
            "severity": "Critique",
            "cause": "Bourrage de l'imprimante tickets.",
            "recommendation": "Contrôler ou remplacer le rouleau papier."
        },

        376: {
            "support": "NCR",
            "status": "En panne",
            "severity": "Moyenne",
            "cause": "Imprimante journal indisponible.",
            "recommendation": "Contrôler l'imprimante journal."
        },

        405: {
            "support": "NCR",
            "status": "En panne",
            "severity": "Critique",
            "cause": "Lecteur de cartes indisponible.",
            "recommendation": "Contrôler le Card Reader."
        },

        398: {
            "support": "NCR",
            "status": "En panne",
            "severity": "Critique",
            "cause": "Clavier EPP indisponible.",
            "recommendation": "Contrôler le PIN Pad."
        },

        394: {
            "support": "NCR",
            "status": "En panne",
            "severity": "Critique",
            "cause": "Blocage du Shutter.",
            "recommendation": "Contrôler le mécanisme du Shutter."
        },

        443: {
            "support": "Logistique",
            "status": "Attention",
            "severity": "Moyenne",
            "cause": "Cassette faible.",
            "recommendation": "Prévoir un réapprovisionnement."
        },

        444: {
            "support": "Logistique",
            "status": "Attention",
            "severity": "Moyenne",
            "cause": "Cassette presque vide.",
            "recommendation": "Réapprovisionner rapidement."
        },

        445: {
            "support": "Logistique",
            "status": "En panne",
            "severity": "Critique",
            "cause": "Cassette indisponible.",
            "recommendation": "Réapprovisionner immédiatement."
        },

        446: {
            "support": "Logistique",
            "status": "En panne",
            "severity": "Critique",
            "cause": "Cassette indisponible.",
            "recommendation": "Réapprovisionner immédiatement."
        },
    }

    @classmethod
    def evaluate(cls, action_id, etat_cloture=None):

        rule = cls.RULES.get(action_id)

        if not rule:
            return {
                "status": "Opérationnel",
                "severity": "Faible",
                "cause": "Aucune anomalie détectée.",
                "recommendation": "Aucune action requise.",
                "support": None,
                "support_contact": None,
            }

        contact = ContactService.get_contact(
            rule["support"]
        )

        result = {
            **rule,
            "support_contact": contact,
        }

        if etat_cloture == 1:
            result["status"] = "Résolu"
            result["recommendation"] = (
                "Incident déjà traité. Consulter l'historique si nécessaire."
            )

        return result