from django.urls import path

from . import views

app_name = "incidents"

urlpatterns = [
    path(
        "",
        views.IncidentsListView.as_view(),
        name="liste",
    ),
]
