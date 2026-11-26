"""Inicio y cierre de sesión (RF-11.1) con las vistas que ya trae Django."""

from django.contrib.auth import views as vistas_auth
from django.urls import path

urlpatterns = [
    path("entrar/", vistas_auth.LoginView.as_view(), name="login"),
    path("salir/", vistas_auth.LogoutView.as_view(), name="logout"),
]
