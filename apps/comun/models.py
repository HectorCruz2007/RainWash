"""Piezas de modelo que comparten varias apps."""

from django.db import models


class Origen(models.TextChoices):
    MANUAL = "manual", "Captura manual"
    ARCHIVO = "archivo", "Archivo importado"
    EXTERNA = "externa", "Fuente externa"
    CALCULADO = "calculado", "Calculado por la plataforma"


class ProcedenciaMixin(models.Model):
    """Dice de dónde salió un dato y si es una medición o una estimación.

    Lo heredan los modelos de datos de entrada (elevación, lluvia, suelo) y los de
    resultados. Así el sistema distingue siempre datos medidos de resultados
    estimados, como pide la consideración de RF-06.
    """

    origen = models.CharField(max_length=10, choices=Origen.choices, default=Origen.MANUAL)
    fuente = models.CharField(
        max_length=120,
        blank=True,
        help_text="Nombre de la fuente o del archivo, por ejemplo: Open-Meteo.",
    )
    fecha_consulta = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Cuándo se descargó o importó el dato.",
    )
    es_estimado = models.BooleanField(
        default=False,
        help_text="Marcado si el valor sale de un modelo y no de una medición directa.",
    )

    class Meta:
        abstract = True
