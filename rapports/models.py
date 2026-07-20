from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Rapport(models.Model):

    class Type(models.TextChoices):
        QUOTIDIEN = "QUOTIDIEN", _("Quotidien")
        HEBDOMADAIRE = "HEBDOMADAIRE", _("Hebdomadaire")
        MENSUEL = "MENSUEL", _("Mensuel")
        ANNUEL = "ANNUEL", _("Annuel")
        PERSONNALISE = "PERSONNALISE", _("Personnalisé")

    class Format(models.TextChoices):
        PDF = "PDF", _("PDF")
        EXCEL = "EXCEL", _("Excel")
        EMAIL = "EMAIL", _("E-mail")

    class Statut(models.TextChoices):
        BROUILLON = "BROUILLON", _("Brouillon")
        GENERATION = "GENERATION", _("En génération")
        GENERE = "GENERE", _("Généré")
        ECHEC = "ECHEC", _("Échec")
        ARCHIVE = "ARCHIVE", _("Archivé")

    titre = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Titre"),
    )
    type_rapport = models.CharField(
        max_length=20,
        choices=Type.choices,
        verbose_name=_("Type"),
    )
    format = models.CharField(
        max_length=10,
        choices=Format.choices,
        default=Format.PDF,
        verbose_name=_("Format"),
    )
    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.BROUILLON,
        verbose_name=_("Statut"),
    )
    date_debut = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date de début"),
    )
    date_fin = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date de fin"),
    )
    parametres = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Paramètres"),
        help_text=_("Filtres et options de génération sérialisés."),
    )
    auteur = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rapports",
        verbose_name=_("Auteur"),
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date de création"),
    )
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Date de modification"),
    )
    date_generation = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Date de génération"),
    )

    class Meta:
        verbose_name = _("Rapport")
        verbose_name_plural = _("Rapports")
        ordering = ["-date_creation"]
        indexes = [
            models.Index(fields=["type_rapport", "statut"], name="idx_rapport_type_statut"),
        ]

    def __str__(self):
        return self.titre or str(self.pk)


class Destinataire(models.Model):

    nom = models.CharField(
        max_length=255,
        verbose_name=_("Nom"),
    )
    email = models.EmailField(
        verbose_name=_("Adresse e-mail"),
    )
    actif = models.BooleanField(
        default=True,
        verbose_name=_("Actif"),
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date de création"),
    )
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Date de modification"),
    )

    class Meta:
        verbose_name = _("Destinataire")
        verbose_name_plural = _("Destinataires")
        ordering = ["nom", "email"]
        constraints = [
            models.UniqueConstraint(
                fields=["email"],
                name="uq_destinataire_email",
            ),
        ]

    def __str__(self):
        return self.nom or self.email


class EmailLog(models.Model):

    class StatutEnvoi(models.TextChoices):
        EN_ATTENTE = "EN_ATTENTE", _("En attente")
        ENVOYE = "ENVOYE", _("Envoyé")
        ECHEC = "ECHEC", _("Échec")
        ANNULE = "ANNULE", _("Annulé")

    rapport = models.ForeignKey(
        to=Rapport,
        on_delete=models.CASCADE,
        related_name="email_logs",
        verbose_name=_("Rapport"),
    )
    destinataire = models.ForeignKey(
        to=Destinataire,
        on_delete=models.CASCADE,
        related_name="email_logs",
        verbose_name=_("Destinataire"),
    )
    statut = models.CharField(
        max_length=20,
        choices=StatutEnvoi.choices,
        default=StatutEnvoi.EN_ATTENTE,
        verbose_name=_("Statut d'envoi"),
    )
    sujet = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Sujet"),
    )
    message_erreur = models.TextField(
        blank=True,
        verbose_name=_("Message d'erreur"),
    )
    reponse_smtp = models.TextField(
        blank=True,
        verbose_name=_("Réponse SMTP"),
        help_text=_("Détail technique de la passerelle de messagerie."),
    )
    date_envoi = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date d'envoi"),
    )
    date_echec = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Date d'échec"),
    )

    class Meta:
        verbose_name = _("Journal d'envoi e-mail")
        verbose_name_plural = _("Journaux d'envoi e-mail")
        ordering = ["-date_envoi"]
        indexes = [
            models.Index(fields=["statut"], name="idx_emaillog_statut"),
        ]

    def __str__(self):
        return _("%(rapport)s → %(destinataire)s (%(statut)s)") % {
            "rapport": self.rapport,
            "destinataire": self.destinataire,
            "statut": self.get_statut_display(),
        }
