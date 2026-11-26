"""Rutas principales. Cada app nueva agrega aquí una línea con su include()."""

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cuentas/", include("apps.cuentas.urls")),
    path("", login_required(TemplateView.as_view(template_name="inicio.html")), name="inicio"),
]
