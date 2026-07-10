from django.db import models


class Fournisseur(models.Model):
    id_fournisseur = models.IntegerField(primary_key=True)
    nom_fournisseur = models.TextField()
    gsm_fournisseur = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = "fournisseur"
        ordering = ["nom_fournisseur"]
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"

    def __str__(self):
        return self.nom_fournisseur


class Filiale(models.Model):
    id_filiale = models.CharField(primary_key=True, max_length=11)
    nom_filiale = models.CharField(max_length=200)
    pays = models.CharField(max_length=20, blank=True, null=True)
    etat_activation = models.IntegerField(default=1)

    class Meta:
        db_table = "filiale"
        ordering = ["nom_filiale"]
        verbose_name = "Filiale"
        verbose_name_plural = "Filiales"

    def __str__(self):
        return self.nom_filiale
    
    
class GAB(models.Model):

    ETAT_CHOICES = [
        ("OPERATIONNEL", "Opérationnel"),
        ("HORS_SERVICE", "Hors service"),
        ("CRITIQUE", "Critique"),
        ("PASSIF", "Passif"),
        ("SUPERVISION", "En supervision"),
    ]

    terminal = models.IntegerField(primary_key=True)

    numero_serie = models.CharField(max_length=50, blank=True, null=True)

    nom_gab = models.CharField(max_length=150, blank=True, null=True)

    date_installation = models.CharField(max_length=50, blank=True, null=True)

    emplacement = models.CharField(max_length=200, blank=True, null=True)

    type_emplacement = models.CharField(max_length=200, blank=True, null=True)

    gestion = models.IntegerField(blank=True, null=True)

    gestionnaire = models.CharField(max_length=200, blank=True, null=True)

    ip_adresse_gab = models.CharField(max_length=150, blank=True, null=True)

    ip_adresse_source = models.CharField(max_length=150, blank=True, null=True)

    type_gab = models.CharField(max_length=15, blank=True, null=True)

    code_bank = models.CharField(max_length=10, blank=True, null=True)

    code_bam = models.IntegerField(blank=True, null=True)

    code_group = models.CharField(max_length=200, blank=True, null=True)

    code_succursale = models.CharField(max_length=10, blank=True, null=True)

    code_agence = models.CharField(max_length=10, blank=True, null=True)

    libelle_agence = models.CharField(max_length=150, blank=True, null=True)

    adresse_gab = models.TextField(blank=True, null=True)

    importance = models.CharField(max_length=2, blank=True, null=True)

    ville = models.CharField(max_length=50, blank=True, null=True)

    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.PROTECT,
        db_column="id_fournisseur",
        related_name="gabs",
        blank=True,
        null=True,
)

    id_activation = models.IntegerField(blank=True, null=True)

    etat = models.CharField(
        max_length=20,
        choices=ETAT_CHOICES,
        default="PASSIF",
    )

    derniere_synchronisation = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "gab"
        ordering = ["terminal"]
        verbose_name = "GAB"
        verbose_name_plural = "GAB"

    def __str__(self):
        return f"{self.terminal} - {self.nom_gab}"