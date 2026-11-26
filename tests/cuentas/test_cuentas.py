import pytest
from django.urls import reverse

from apps.cuentas.models import Rol

pytestmark = pytest.mark.django_db

CLAVE = "clave-de-prueba-123"


@pytest.fixture
def ana(django_user_model):
    return django_user_model.objects.create_user("ana", password=CLAVE)


def test_hay_cinco_roles():
    assert len(Rol.choices) == 5


def test_usuario_nuevo_empieza_con_rol_de_consulta(ana):
    assert ana.rol == Rol.CONSULTA


def test_superusuario_recibe_rol_de_administrador(django_user_model):
    jefe = django_user_model.objects.create_superuser("jefe", password=CLAVE)
    assert jefe.rol == Rol.ADMINISTRADOR


def test_inicio_pide_sesion_a_un_visitante(client):
    respuesta = client.get(reverse("inicio"))
    assert respuesta.status_code == 302
    assert respuesta.url.startswith(reverse("login"))


def test_iniciar_sesion_lleva_al_inicio_y_muestra_el_rol(client, ana):
    respuesta = client.post(
        reverse("login"), {"username": "ana", "password": CLAVE}, follow=True
    )
    assert respuesta.redirect_chain[-1][0] == reverse("inicio")
    assert "Usuario de consulta" in respuesta.content.decode()


def test_clave_incorrecta_no_inicia_sesion(client, ana):
    respuesta = client.post(reverse("login"), {"username": "ana", "password": "otra"})
    assert respuesta.status_code == 200
    assert respuesta.context["form"].non_field_errors()
    assert client.get(reverse("inicio")).status_code == 302


def test_cerrar_sesion_vuelve_a_pedir_acceso(client, ana):
    client.force_login(ana)
    respuesta = client.post(reverse("logout"))
    assert respuesta.status_code == 302
    assert client.get(reverse("inicio")).status_code == 302
