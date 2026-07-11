from django.urls import path

from . import views

app_name = "gab"

urlpatterns = [
    path("", views.liste_gab, name="liste_gab"),
    path("api/<int:terminal>/", views.gab_api_detail, name="gab_api_detail"),
]