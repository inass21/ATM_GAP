from django.urls import path

from .views import (
    DashboardView,
    CarteView,
    DeclarationIncidentView,
)


app_name = "dashboard"

urlpatterns = [
    path(
        "",
        DashboardView.as_view(),
        name="index",
    ),
    path(
        "carte/",
        CarteView.as_view(),
        name="carte",
    ),
    path(
        "declaration-incident/",
        DeclarationIncidentView.as_view(),
        name="declaration_incident",
    ),
]
