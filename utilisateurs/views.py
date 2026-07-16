from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from .models import Utilisateur
from .forms import LoginForm

class ConnexionView(LoginView):
    template_name = "authentification/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True
    def get_success_url(self):
        # Redirection temporaire vers le Parc GAB (le Dashboard principal
        # n'est pas encore développé). À réviser une fois le Dashboard prêt.
        return reverse("gab:liste_gab")

class DeconnexionView(LogoutView):
    next_page = reverse_lazy("login")
