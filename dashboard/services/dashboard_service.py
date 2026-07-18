from gab.models import GAB
from gab.services.availability import AvailabilityService
from gab.models_source import NewIncidentGab

from dashboard.services.map_service import MapService

from statistiques.services.kpi_service import KPIService
from statistiques.services.evolution_service import EvolutionService
from statistiques.services.health_service import HealthService

from statistiques.services.filter_service import FilterService


class DashboardService:

    # Le Dashboard ne fait qu'orchestrer les services existants (MapService,
    # KPIService, EvolutionService, HealthService, AvailabilityService).
    # Aucune formule n'est recalculee ici : on reutilise les sources uniques
    # de verite deja en place dans le projet.

    @staticmethod
    def get_context(filters=None):

        kpis = KPIService.get_kpis(filters)

        evolution = EvolutionService.get_evolution(filters)

        health_scores = HealthService.get_health_scores(filters)

        global_health = HealthService.get_global_health(
            filters, scores=health_scores
        )

        regions = MapService.get_regions_summary(filters)

        # Tableau des GAB les plus critiques : on reprend le classement
        # "pires scores" de HealthService (deja trie par score croissant),
        # mais on ne garde QUE les GAB reellement en etat "Critique"
        # pour ne pas afficher des GAB sains sous un faux intitule.
        critical_gabs = [
            g for g in sorted(
                health_scores,
                key=lambda x: x["score"],
            )
            if g["status"] == "Critique"
        ][:8]

        # Indicateurs de supervision tires du KPI + etat du parc.
        operational_gab = kpis.get("operational_gab", 0)
        offline_gab = kpis.get("offline_gab", 0)
        critical_gab = kpis.get("critical_gab", 0)
        passive_gab = kpis.get("passive_gab", 0)
        total_gab = kpis.get("total_gab", 0)

        maintenance_gab = passive_gab

        sla_depasse = sum(
            1 for score in health_scores if score["status"] == "Critique"
        )

        # Vraies valeurs metier (lecture directe de la base) :
        #  - incidents ouverts     : etat_incident = 0
        #  - interventions en cours: etat_cloture  = 0
        incidents_qs = FilterService.get_incidents_queryset(filters)
        interventions_qs = FilterService.get_interventions_queryset(filters)

        open_incidents = incidents_qs.filter(etat_incident=0).count()

        interventions_en_cours = interventions_qs.filter(
            etat_cloture=0
        ).count()

        # Compteur "aujourd'hui" : la base n'a pas forcement d'incidents a la
        # date du jour. On prend donc la DERNIERE date reellement presente en
        # base (le jour d'activite le plus recent) et on compte ses incidents.
        last_incident_date = (
            incidents_qs
            .exclude(date_arrete__isnull=True)
            .order_by("-date_arrete")
            .values_list("date_arrete", flat=True)
            .first()
        )

        if last_incident_date is not None:
            incidents_today = incidents_qs.filter(
                date_arrete__date=last_incident_date.date()
            ).count()
        else:
            incidents_today = 0

        # Derniere synchronisation connue sur l'ensemble du parc.
        last_sync = (
            GAB.objects
            .exclude(derniere_synchronisation__isnull=True)
            .order_by("-derniere_synchronisation")
            .values_list("derniere_synchronisation", flat=True)
            .first()
        )

        # Feed live : incidents ouverts les plus recents (etat_incident = 0),
        # tries par date d'arret decroissante. Pas de donnees fictives :
        # on lit directement new_incident_gab.
        live_feed = list(
            NewIncidentGab.objects
            .filter(etat_incident=0)
            .select_related()
            .order_by("-date_arrete")[:12]
        )

        live_feed_serialized = []
        for incident in live_feed:
            gab = (
                GAB.objects
                .filter(terminal=incident.id_gab)
                .first()
            )
            live_feed_serialized.append({
                "id_incident": incident.id_incident,
                "terminal": incident.id_gab,
                "terminal_label": (
                    gab.terminal if gab else incident.id_gab
                ),
                "nom_gab": (
                    gab.nom_gab if gab else None
                ),
                "ville": (
                    gab.ville if gab else None
                ),
                "agence": (
                    gab.libelle_agence if gab else None
                ),
                "date_arrete": incident.date_arrete,
                "num_tiket": incident.num_tiket,
                "num_affectation": incident.num_affectation,
            })

        # Repartition de l'etat du parc pour le doughnut / la legende.
        distribution = {
            "operational": operational_gab,
            "maintenance": maintenance_gab,
            "offline": offline_gab,
            "critical": critical_gab,
        }

        # Statut global du reseau, calcule a partir de la disponibilite
        # reelle (KPI) vs l'objectif 99%. Sert a piloter l'affichage
        # (pastille du header + libelle de la carte Disponibilite).
        availability = kpis.get("availability", 0) or 0
        NETWORK_OBJECTIVE = 99.0
        if availability >= NETWORK_OBJECTIVE:
            network_state = "OPERATIONNEL"
            network_status = "STABLE"
        elif availability >= 75.0:
            network_state = "DEGRADE"
            network_status = "DEGRADE"
        else:
            network_state = "CRITIQUE"
            network_status = "CRITIQUE"

        return {
            "kpis": kpis,
            "global_health": global_health,
            "evolution": evolution,
            "regions": regions,
            "critical_gabs": critical_gabs,
            "distribution": distribution,
            "sla_depasse": sla_depasse,
            "live_feed": live_feed_serialized,
            "last_sync": last_sync,
            "last_incident_date": last_incident_date,
            "network_state": network_state,
            "network_status": network_status,
            "network_objective": NETWORK_OBJECTIVE,
            "total_gab": total_gab,
            "open_incidents": open_incidents,
            "interventions_en_cours": interventions_en_cours,
            "incidents_today": incidents_today,
        }
