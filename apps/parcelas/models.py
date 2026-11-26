"""Parcelas agrícolas que se analizan en la plataforma (RF-01)."""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


def validar_poligono_geojson(valor):
    """Revisa que el valor tenga la forma de un polígono GeoJSON."""
    if not isinstance(valor, dict) or valor.get("type") != "Polygon":
        raise ValidationError('La geometría debe ser un GeoJSON de tipo "Polygon".')
    anillos = valor.get("coordinates")
    exterior = anillos[0] if isinstance(anillos, list) and anillos else None
    if not isinstance(exterior, list) or len(exterior) < 4:
        raise ValidationError(
            "El polígono necesita al menos 4 posiciones (la última repite la primera)."
        )


class Parcela(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField("descripción", blank=True)
    propietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="parcelas",
    )
    geometria = models.JSONField(
        "geometría",
        null=True,
        blank=True,
        validators=[validar_poligono_geojson],
        help_text="Polígono GeoJSON en longitud y latitud (WGS 84).",
    )
    # La superficie declarada la escribe el usuario (RF-01.6); la calculada
    # la obtiene el sistema a partir del polígono (RF-01.7).
    superficie_declarada_ha = models.FloatField(
        "superficie declarada (ha)",
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    superficie_calculada_ha = models.FloatField(
        "superficie calculada (ha)",
        null=True,
        blank=True,
        editable=False,
    )
    creada = models.DateTimeField(auto_now_add=True)
    actualizada = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["propietario", "nombre"],
                name="parcela_nombre_unico_por_propietario",
            ),
        ]

    def __str__(self):
        return self.nombre
