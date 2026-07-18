from django.urls import path
from .views import ConnexionView, DeconnexionView

app_name = "utilisateurs"

urlpatterns = [
    path("login/", ConnexionView.as_view(), name="login"),
    path("logout/", DeconnexionView.as_view(), name="logout"),
]