from django.contrib import admin

from .models import Parcela


@admin.register(Parcela)
class ParcelaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "propietario", "superficie_declarada_ha", "actualizada")
    list_filter = ("propietario",)
    search_fields = ("nombre", "descripcion")
    readonly_fields = ("superficie_calculada_ha", "creada", "actualizada")
