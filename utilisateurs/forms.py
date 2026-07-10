from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


class LoginForm(AuthenticationForm):

    error_messages = {
        "invalid_login": "Nom d'utilisateur ou mot de passe incorrect.",
        "inactive": "Ce compte est désactivé.",
    }

    username = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
           
        })
    )

    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            
        })
    )