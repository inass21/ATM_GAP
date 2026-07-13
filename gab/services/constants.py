"""
Constantes métier utilisées par le module Diagnostic.
"""

# ==========================================================
# Etats
# ==========================================================

STATUS_OPERATIONAL = "Opérationnel"
STATUS_WARNING = "Attention"
STATUS_FAILED = "En panne"
STATUS_UNKNOWN = "Inconnu"


# ==========================================================
# Niveaux de gravité
# ==========================================================

SEVERITY_LOW = "Faible"
SEVERITY_MEDIUM = "Moyenne"
SEVERITY_HIGH = "Critique"


# ==========================================================
# Mapping composants -> Actions
# ==========================================================

COMPONENT_ACTIONS = {

    "card_reader": [
        405,
    ],

    "printer": [
        376,
        379,
        421,
    ],

    "epp": [
        398,
    ],

    "shutter": [
        394,
    ],

    "cash_dispenser": [
        382,
        383,
        384,
        390,
        392,
        424,
        425,
        426,
        427,
        443,
        444,
        445,
        446,
    ],

    "connection": [
        419,
        434,
    ],
}