from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario

SECCION_ROL = ("Rol en la plataforma", {"fields": ("rol",)})


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ("username", "email", "rol", "is_staff", "is_active")
    list_filter = ("rol", "is_staff", "is_active")
    fieldsets = UserAdmin.fieldsets + (SECCION_ROL,)
    add_fieldsets = UserAdmin.add_fieldsets + (SECCION_ROL,)
