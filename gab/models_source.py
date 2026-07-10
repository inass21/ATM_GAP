# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class NewListGab(models.Model):
    terminal = models.IntegerField(primary_key=True)
    id_terminal_xfs = models.IntegerField(blank=True, null=True)
    id_traitement = models.IntegerField()
    state_aid = models.IntegerField()
    state_calcul = models.IntegerField()
    profile_withrawal = models.IntegerField()
    state_autoris_supply = models.IntegerField()
    date_last_update_autorise_supply = models.DateTimeField()
    date_last_supply_ordered = models.DateTimeField()
    date_up_supply = models.DateTimeField()
    nb_max_bills_100 = models.IntegerField()
    nb_max_bills_200 = models.IntegerField()
    nb_max_bills_50 = models.IntegerField()
    nb_max_bills_20 = models.IntegerField()
    nbr_free_supply = models.IntegerField()
    nbr_free_transport = models.IntegerField()
    transport_cost = models.IntegerField()
    supply_cost = models.IntegerField()
    cost_exter = models.IntegerField()
    avg_consum_global = models.IntegerField()
    max_consum_50 = models.IntegerField()
    max_consum_20 = models.IntegerField()
    max_supply = models.IntegerField()
    date_ajout = models.DateTimeField()
    numero_serie = models.CharField(max_length=50)
    cdf = models.CharField(max_length=50)
    date_installation = models.CharField(max_length=50)
    emplacement = models.CharField(max_length=200)
    type_emplacement = models.CharField(max_length=200)
    gestion = models.IntegerField()
    gestionnaire = models.CharField(max_length=200)
    nom_gab = models.CharField(max_length=150)
    ip_adresse_gab = models.CharField(max_length=150)
    ip_adresse_source = models.CharField(max_length=150)
    type_gab = models.CharField(max_length=15)
    code_bank = models.CharField(max_length=10)
    code_bam = models.IntegerField()
    code_group = models.CharField(max_length=200)
    code_succursale = models.CharField(max_length=10)
    code_agence = models.CharField(max_length=10)
    libelle_agence = models.CharField(max_length=150)
    adresse_gab = models.TextField()
    importance = models.CharField(db_column='Importance', max_length=2)  # Field name made lowercase.
    id_fournisseur = models.IntegerField()
    id_prestataire = models.IntegerField()
    ville = models.CharField(max_length=50)
    var = models.IntegerField()
    id_activation = models.IntegerField()
    id_activ_depot_argent = models.IntegerField()
    id_activ_depot_cheque = models.IntegerField()
    last_date_desactivation = models.DateTimeField()
    id_strategiques = models.IntegerField()
    id_profil = models.IntegerField()
    param_statique = models.IntegerField()
    appel_web_service = models.IntegerField()
    id_utilisateur = models.IntegerField()
    acces_gab = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'new_list_gab'


class NewFiliale(models.Model):
    id_filiale = models.CharField(primary_key=True, max_length=11)
    nom_filiale = models.CharField(max_length=200)
    id_filiale2 = models.CharField(max_length=50)
    id_filiale3 = models.CharField(max_length=20)
    nom_filiale2 = models.CharField(max_length=30)
    pays = models.CharField(db_column='PAYS', max_length=20)  # Field name made lowercase.
    etat_activation = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'new_filiale'


class NewListFournisseur(models.Model):
    id_fournisseur = models.AutoField(primary_key=True)
    nom_fournisseur = models.TextField()
    gsm_fournisseur = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'new_list_fournisseur'


class ActivationGabs(models.Model):
    id_activation = models.AutoField(primary_key=True)
    id_gab = models.IntegerField()
    date_activ_desac = models.DateTimeField()
    activ_desact = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'activation_gabs'