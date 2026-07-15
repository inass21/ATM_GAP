from django.urls import path

from .views import (
    ExportStatisticsExcelView,
    StatisticsDashboardView,
)

app_name = "statistiques"

urlpatterns = [

    path(
        "",
        StatisticsDashboardView.as_view(),
        name="dashboard",
    ),

    path(
        "export/excel/",
        ExportStatisticsExcelView.as_view(),
        name="export_excel",
    ),

]