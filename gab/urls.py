from django.urls import path

from . import views

app_name = "gab"

urlpatterns = [
   
    path("", views.liste_gab, name="liste_gab"),

    path(
        "api/<int:terminal>/",
        views.gab_api_detail,
        name="gab_api_detail",
    ),

    path(
        "diagnostic/<int:gab_id>/",
        views.diagnostic_page,
        name="diagnostic",
    ),

    path(
        "api/diagnostic/<int:gab_id>/",
        views.diagnostic_api,
        name="diagnostic_api",
    ),
]
