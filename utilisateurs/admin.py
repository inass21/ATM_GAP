from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Utilisateur, Filiale


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "role",
        "is_active",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
    )

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )

    ordering = ("username",)


@admin.register(Filiale)
class FilialeAdmin(admin.ModelAdmin):
    list_display = (
        "id_filiale",
        "nom_filiale",
        "pays",
        "etat_activation",
    )

    search_fields = (
        "id_filiale",
        "nom_filiale",
    )

    list_filter = (
        "etat_activation",
    )

    ordering = (
        "nom_filiale",
    )