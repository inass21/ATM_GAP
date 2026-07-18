"""Signaux d'invalidation du cache des statistiques.

Quand une donnee source change (GAB, incident, intervention), on vide le
cache des statistiques pour forcer un recalcul a la prochaine requete.
Le cache est sinon rafraichi automatiquement toutes les 5 minutes
(STATISTICS_CACHE_TTL).
"""

from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import receiver

from gab.models import GAB
from statistiques.services.statistics_service import (
    invalidate_statistics_cache,
)


@receiver(post_save, sender=GAB)
@receiver(post_delete, sender=GAB)
def _invalidate_on_gab_change(sender, instance, **kwargs):
    invalidate_statistics_cache()


def invalidate_on_source_change():
    """A appeler apres toute mutation sur les tables legacy non gerees
    (new_incident_gab, new_intevention_incident) ou apres un sync."""
    invalidate_statistics_cache()
