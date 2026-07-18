from django.urls import path

from . import views

app_name = "interventions"

urlpatterns = [
    path(
        "",
        views.InterventionsListView.as_view(),
        name="liste",
    ),
]
