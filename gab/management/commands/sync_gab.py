from django.core.management.base import BaseCommand
from django.db import transaction
from gab.models import Filiale, Fournisseur, GAB
from gab.models_source import (
    ActivationGabs,
    NewFiliale,
    NewListFournisseur,
    NewListGab,
)


class Command(BaseCommand):
    help = "Synchronisation des données depuis la base entreprise"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("=== Synchronisation ASIMS ==="))

        with transaction.atomic():
            self.sync_filiales()
            self.sync_fournisseurs()
            self.sync_gab()

        self.stdout.write(self.style.SUCCESS("Synchronisation terminée."))

    # FILIALES

    def sync_filiales(self):

        for filiale in NewFiliale.objects.all().iterator():

            Filiale.objects.update_or_create(
                id_filiale=filiale.id_filiale,
                defaults={
                    "nom_filiale": filiale.nom_filiale,
                    "pays": filiale.pays,
                    "etat_activation": filiale.etat_activation,
                },
            )

        self.stdout.write(self.style.SUCCESS("✔ Filiales synchronisées"))

    def sync_fournisseurs(self):

        for fournisseur in NewListFournisseur.objects.all().iterator():

            Fournisseur.objects.update_or_create(
                id_fournisseur=fournisseur.id_fournisseur,
                defaults={
                    "nom_fournisseur": fournisseur.nom_fournisseur,
                    "gsm_fournisseur": fournisseur.gsm_fournisseur,
                },
            )

        self.stdout.write(self.style.SUCCESS("✔ Fournisseurs synchronisés"))

    # GAB

    def sync_gab(self):

        self.stdout.write(
            self.style.WARNING("Synchronisation des GAB ...")
        )

        created = 0
        updated = 0
        errors = 0

        for source_gab in NewListGab.objects.all().iterator():
            fournisseur = Fournisseur.objects.filter(id_fournisseur=source_gab.id_fournisseur).first()
            if fournisseur is None:
                self.stdout.write(self.style.ERROR(
                    f"GAB {source_gab.terminal} : Fournisseur introuvable (id_fournisseur={source_gab.id_fournisseur})."
                ))
                errors += 1
                continue

            etat = self.compute_etat(source_gab)
            _, created_flag = GAB.objects.update_or_create(
                terminal=source_gab.terminal,
                defaults={
                    "numero_serie": source_gab.numero_serie,
                    "nom_gab": source_gab.nom_gab,
                    "date_installation": source_gab.date_installation,
                    "emplacement": source_gab.emplacement,
                    "type_emplacement": source_gab.type_emplacement,
                    "gestion": source_gab.gestion,
                    "gestionnaire": source_gab.gestionnaire,
                    "ip_adresse_gab": source_gab.ip_adresse_gab,
                    "ip_adresse_source": source_gab.ip_adresse_source,
                    "type_gab": source_gab.type_gab,
                    "code_bank": source_gab.code_bank,
                    "code_bam": source_gab.code_bam,
                    "code_group": source_gab.code_group,
                    "code_succursale": source_gab.code_succursale,
                    "code_agence": source_gab.code_agence,
                    "libelle_agence": source_gab.libelle_agence,
                    "adresse_gab": source_gab.adresse_gab,
                    "importance": source_gab.importance,
                    "ville": source_gab.ville,
                    "fournisseur": fournisseur,
                    "id_activation": source_gab.id_activation,

                    "etat": etat,
                },
            )

            if created_flag:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"✔ {created} GAB créés, {updated} GAB mis à jour"))
        return created, updated, errors

    def compute_etat(self, source_gab):
        activation = (
            ActivationGabs.objects
            .filter(id_gab=source_gab.terminal)
            .order_by("-date_activ_desac")
            .first()
        )

        if activation is None:
            return "PASSIF"

        if activation.activ_desact == 1:
            return "OPERATIONNEL"
        if activation.activ_desact == 2:
            return "PASSIF"

        return "PASSIF"
