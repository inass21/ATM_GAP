from django.urls import path

from . import views

app_name = "rapports"

urlpatterns = [
    path(
        "",
        views.RapportsListView.as_view(),
        name="liste",
    ),
]
