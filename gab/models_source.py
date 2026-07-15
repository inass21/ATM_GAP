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

class NewIncidentGab(models.Model):
    id_incident = models.AutoField(primary_key=True)
    id_gab = models.IntegerField()
    clo_auto = models.IntegerField()
    last_trans = models.DateTimeField(db_column='last_Trans')  # Field name made lowercase.
    date_arrete = models.DateTimeField()
    date_prise_en_charge_contractuelle = models.DateTimeField()
    date_prise_en_charge = models.DateTimeField()
    date_prise_charge_bcp = models.DateTimeField()
    date_prise_charge_gestionnaire = models.DateTimeField()
    num_tiket = models.CharField(max_length=15)
    num_affectation = models.CharField(max_length=50)
    num_paradigme = models.CharField(max_length=20)
    date_remise = models.DateTimeField()
    date_derniere_interv = models.DateTimeField()
    date_derniere_rappel = models.DateTimeField()
    etat_incident = models.IntegerField()
    remarque_press = models.TextField()
    remarque_frss = models.TextField()
    rapport_technique_excel = models.IntegerField()
    id_indisponibilite = models.IntegerField()
    id_gab_sensible = models.IntegerField()
    cd_filiale = models.CharField(max_length=10)
    cd_region = models.CharField(max_length=10)
    cd_banque = models.CharField(max_length=10)
    cd_agence = models.CharField(max_length=10)
    nom_agence = models.CharField(max_length=150)
    cd_prestataire = models.IntegerField()
    cd_fournisseur = models.IntegerField()
    cd_arret_fonctionnelle = models.IntegerField()
    id_categories_fonctionnelle = models.IntegerField()
    cd_arret_technique = models.IntegerField()
    id_categories_technique = models.IntegerField()
    id_action_fonctionelle = models.IntegerField()
    id_niveau_fonctionelle = models.IntegerField()
    id_action_technique = models.IntegerField()
    id_niveau_technique = models.IntegerField()
    id_facturable = models.IntegerField()
    id_activation = models.IntegerField()
    id_strategiques = models.IntegerField()
    id_classement = models.IntegerField()
    etat_stat = models.IntegerField()
    appelagence = models.IntegerField()
    montant_c1 = models.IntegerField()
    etat_c1 = models.CharField(max_length=2)
    montant_c2 = models.IntegerField()
    etat_c2 = models.CharField(max_length=2)
    montant_c3 = models.IntegerField()
    etat_c3 = models.CharField(max_length=2)
    montant_c4 = models.IntegerField()
    etat_c4 = models.CharField(max_length=2)
    etat_cas_rejet = models.CharField(max_length=2)
    etat_sep = models.CharField(max_length=2)
    etat_lecteur = models.CharField(max_length=2)
    etat_journal = models.CharField(max_length=2)
    etat_pinpad = models.CharField(max_length=2)
    etat_epp = models.CharField(max_length=2)
    etat_pc = models.CharField(max_length=2)
    last_event = models.CharField(max_length=10)
    last_inserv = models.DateTimeField()
    last_event_date = models.DateTimeField()
    up_last_trans = models.DateTimeField(db_column='up_last_Trans')  # Field name made lowercase.
    if_chgmt_montant = models.IntegerField()
    date_chgmt = models.DateTimeField()
    m_c1_chgmt = models.IntegerField()
    m_c2_chgmt = models.IntegerField()
    m_c3_chgmt = models.IntegerField()
    m_c4_chgmt = models.IntegerField()
    s_c1_chgmt = models.CharField(max_length=2)
    s_c2_chgmt = models.CharField(max_length=2)
    s_c3_chgmt = models.CharField(max_length=2)
    s_c4_chgmt = models.CharField(max_length=2)
    last_inservice_cloture = models.DateTimeField(db_column='last_InService_cloture')  # Field name made lowercase.
    trans_caused_cloture = models.DateTimeField(db_column='Trans_caused_cloture')  # Field name made lowercase.
    date_actuel_cloture = models.DateTimeField()
    statut_connex = models.IntegerField()
    code_screenshot = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'new_incident_gab'


class NewInteventionIncident(models.Model):
    id_action_interv = models.AutoField(primary_key=True)
    id_incident = models.IntegerField()
    id_gab = models.IntegerField()
    id_gab_powerdcard = models.IntegerField()
    nomgab = models.CharField(max_length=50)
    cd_agence = models.CharField(max_length=10)
    nom_agence = models.CharField(max_length=20)
    cd_region_iprc = models.IntegerField()
    id_fournisseur = models.IntegerField()
    id_categories = models.IntegerField()
    responsable = models.CharField(max_length=20)
    date_action = models.DateTimeField()
    date_prise_en_charge = models.DateTimeField()
    date_prise_en_charge2 = models.DateTimeField()
    date_prise_charge_gestionnaire = models.DateTimeField()
    num_affectation = models.CharField(max_length=50)
    id_affectation = models.IntegerField()
    gsm_personne_avise = models.IntegerField()
    commentaire = models.TextField(db_column='Commentaire')  # Field name made lowercase.
    degre_appel = models.IntegerField()
    type_contact = models.CharField(max_length=150)
    etat_contact = models.IntegerField()
    personne_avisee = models.CharField(max_length=300)
    id_action_intervention = models.IntegerField()
    id_niveau_intervention = models.IntegerField()
    details = models.CharField(max_length=200)
    last_trans = models.DateTimeField(db_column='last_Trans')  # Field name made lowercase.
    etat_cloture = models.IntegerField()
    date_cloture = models.DateTimeField()
    date_rappel = models.DateTimeField()
    nbr_tentative = models.IntegerField()
    nbr_escalade = models.IntegerField()
    id_utilisateur = models.IntegerField()
    id_etat_action = models.IntegerField()
    remarque = models.TextField()
    note = models.TextField()
    degre_intervention = models.IntegerField()
    motif_cloture = models.CharField(max_length=20)
    auto_cloture = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'new_intevention_incident'


class NewActionIntervention(models.Model):
    id_intevention = models.AutoField(primary_key=True)
    event = models.CharField(max_length=25, db_collation='utf8_bin')
    msg = models.CharField(max_length=200, db_collation='utf8_bin')
    libelle_intevention = models.CharField(unique=True, max_length=80, db_collation='utf8_bin')
    libelle_intevention_eng = models.CharField(max_length=80)
    affiche_rapport_technique = models.IntegerField()
    retrait_argent = models.IntegerField()
    depot_argent = models.IntegerField()
    depot_cheque = models.IntegerField()
    autre_transactions = models.IntegerField()
    indisponibilite = models.IntegerField()
    degre = models.IntegerField()
    type_arret = models.IntegerField()
    id_categories = models.IntegerField()
    id_facturations = models.IntegerField()
    auto_mail = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'new_action_intervention'
class NewLibelleTypeContact(models.Model):
    id_type = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=50)
    libelle2 = models.CharField(max_length=20)
    libelle_eng = models.CharField(max_length=50)
    contact_nom = models.CharField(max_length=150, blank=True, null=True)
    gsm_contact = models.CharField(max_length=30, blank=True, null=True)
    cal_jour_ouvrable_sla = models.IntegerField()
    duree_sla = models.CharField(max_length=150)
    duree_rappel_sla = models.IntegerField()
    duree_minute = models.IntegerField()
    heure_rappel = models.IntegerField()
    heure_fin = models.IntegerField()
    duree_travail_minute = models.IntegerField()
    duree_hors_travail = models.IntegerField()
    aa_mail = models.TextField()
    cc_mail = models.TextField()
    born_debut_contrac = models.TimeField()
    born_fin_contrac = models.TimeField()
    mode_calcul_date_remise_contrac = models.IntegerField()
    etat_mail_auto = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'new_libelle_type_contact'

class NewCategorieIntervention(models.Model):
    id_categorie = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=100)
    libelle_eng = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "new_categorie_intervention"