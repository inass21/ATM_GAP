from django.urls import path

from .views import StatisticsDashboardView

app_name = "statistiques"

urlpatterns = [

    path(
        "",
        StatisticsDashboardView.as_view(),
        name="dashboard",
    ),

]