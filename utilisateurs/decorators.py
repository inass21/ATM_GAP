from functools import wraps
from django.shortcuts import redirect
from .models import Utilisateur


def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            # Utilisateur non connecté
            if not request.user.is_authenticated:
                return redirect("login")

            # L'administrateur a accès à toutes les vues
            if request.user.role == Utilisateur.Role.ADMINISTRATEUR:
                return view_func(request, *args, **kwargs)

            # Vérification du rôle demandé
            if request.user.role != required_role:
                return redirect("login")

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator