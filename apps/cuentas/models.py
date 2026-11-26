"""Usuarios de la plataforma y sus roles (RF-11)."""

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class Rol(models.TextChoices):
    """Los cinco tipos de usuario que define el documento del proyecto."""

    ADMINISTRADOR = "administrador", "Administrador"
    TECNICO = "tecnico", "Técnico agrícola"
    ANALISTA = "analista", "Analista hidrológico"
    PRODUCTOR = "productor", "Productor agrícola"
    CONSULTA = "consulta", "Usuario de consulta"


class GestorUsuarios(UserManager):
    def create_superuser(self, username, email=None, password=None, **campos):
        campos.setdefault("rol", Rol.ADMINISTRADOR)
        return super().create_superuser(username, email, password, **campos)


class Usuario(AbstractUser):
    """Usuario de Django con un rol. Un usuario nuevo empieza con el rol de menor acceso."""

    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.CONSULTA)

    objects = GestorUsuarios()

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
