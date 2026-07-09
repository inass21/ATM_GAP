from django.db import models
from django.contrib.auth.models import AbstractUser


class Filiale(models.Model):
    id_filiale = models.CharField(primary_key=True, max_length=11)
    nom_filiale = models.CharField(max_length=200)
    pays = models.CharField(db_column="PAYS", max_length=20)
    etat_activation = models.IntegerField()

    class Meta:
        managed = False
        db_table = "new_filiale"

    def __str__(self):
        return self.nom_filiale


class Utilisateur(AbstractUser):

    class Role(models.TextChoices):
        ADMINISTRATEUR = "ADMIN", "Administrateur"
        SUPERVISEUR = "SUPERVISEUR", "Superviseur"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.SUPERVISEUR,
    )

    filiale_rattachee = models.CharField(
    max_length=11,
    null=True,
    blank=True,
    verbose_name="Filiale"
)

    email = models.EmailField(
        unique=True,
        blank=False,
    )

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return self.get_full_name() or self.username